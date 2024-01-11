// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { Duration } from "aws-cdk-lib";
import { Bucket } from "aws-cdk-lib/aws-s3";
import {
  IntegrationPattern,
  JsonPath,
  Map,
  StateMachine,
  TaskInput,
  TaskStateBase,
} from "aws-cdk-lib/aws-stepfunctions";
import {
  LambdaInvoke,
  StepFunctionsStartExecution,
} from "aws-cdk-lib/aws-stepfunctions-tasks";
import { Construct } from "constructs";
import { FormDataExtractionStateMachine } from "./form-data-extraction-state-machine";
import { Table } from "../../common/dynamodb/table";
import {
  PythonLibLambda,
  PythonLibLambdaProps,
} from "../../common/lambda/python-lib-lambda";
import { grantPublishMetrics } from "../../common/metrics/permissions";
import { TextractStateMachine } from "../textract/textract-state-machine";

export interface DocumentIngestionStateMachineProps {
  readonly sourceBucket: Bucket;
  readonly documentMetadataTable: Table;
  readonly formMetadataTable: Table;
  readonly formSchemaTable: Table;
}

/**
 * State machine to orchestrate document ingestion, extracting individual forms from documents and triggering
 * form data extraction for each.
 */
export class DocumentIngestionStateMachine extends Construct {
  public readonly stateMachine: StateMachine;

  constructor(
    scope: Construct,
    id: string,
    {
      sourceBucket,
      documentMetadataTable,
      formMetadataTable,
      formSchemaTable,
    }: DocumentIngestionStateMachineProps,
  ) {
    super(scope, id);

    const buildLambda = (
      handler: string,
      extraProps?: Omit<PythonLibLambdaProps, "handler">,
    ) =>
      new PythonLibLambda(this, handler, {
        handler: `ingestion_state_machine/${handler}`,
        timeout: Duration.minutes(15),
        environment: {
          ...documentMetadataTable.environment,
          ...formMetadataTable.environment,
          ...formSchemaTable.environment,
        },
        ...extraProps,
      });

    const onErrorLambda = buildLambda("on_error");
    documentMetadataTable.grantReadWriteData(onErrorLambda);
    grantPublishMetrics(onErrorLambda);

    const onError = new LambdaInvoke(this, "OnError", {
      lambdaFunction: onErrorLambda,
      payload: TaskInput.fromObject({
        payload: JsonPath.stringAt("$.Payload"),
        document_id: JsonPath.stringAt("$.Payload.DocumentId"),
        error_details: JsonPath.stringAt("$.ErrorDetails"),
      }),
      resultPath: JsonPath.DISCARD,
    });

    const withErrorHandler = (state: TaskStateBase) =>
      state.addCatch(onError, {
        resultPath: "$.ErrorDetails",
      });

    const textractStateMachine = new TextractStateMachine(
      this,
      "TextractStateMachine",
      {
        sourceBucket,
      },
    );

    const saveClassifiedFormsLambda = buildLambda("save_classified_forms");
    sourceBucket.grantReadWrite(saveClassifiedFormsLambda);
    formMetadataTable.grantReadWriteData(saveClassifiedFormsLambda);
    documentMetadataTable.grantReadWriteData(saveClassifiedFormsLambda);
    formSchemaTable.grantReadData(saveClassifiedFormsLambda);
    grantPublishMetrics(saveClassifiedFormsLambda);

    const saveClassifiedForms = withErrorHandler(
      new LambdaInvoke(this, "SaveClassifiedForms", {
        lambdaFunction: saveClassifiedFormsLambda,
        payload: TaskInput.fromObject({
          document_id: JsonPath.stringAt("$.Payload.DocumentId"),
          schema_id: JsonPath.stringAt("$.Payload.SchemaId"),
          document_location: JsonPath.stringAt("$.Payload.DocumentLocation"),
          caller: JsonPath.stringAt("$.Payload.CallingUser"),
        }),
        payloadResponseOnly: true,
        resultPath: "$.Payload.SaveClassifiedFormsOutput",
      }),
    );

    const formDataExtractionStateMachine = new FormDataExtractionStateMachine(
      this,
      "FormDataExtractionStateMachine",
      {
        sourceBucket,
        documentMetadataTable,
        formMetadataTable,
        formSchemaTable,
        textractStateMachine,
      },
    );

    const extractFormData = new StepFunctionsStartExecution(
      this,
      "ExtractFormData",
      {
        stateMachine: formDataExtractionStateMachine.stateMachine,
        input: TaskInput.fromObject({
          Payload: {
            Form: JsonPath.stringAt("$"),
          },
        }),
        integrationPattern: IntegrationPattern.RUN_JOB,
        resultPath: "$.Payload.ExtractFormDataOutput",
      },
    );

    this.stateMachine = new StateMachine(
      this,
      "DocumentIngestionStateMachine",
      {
        definition: saveClassifiedForms.next(
          new Map(this, "ForEachClassifiedForm", {
            itemsPath: JsonPath.stringAt(
              "$.Payload.SaveClassifiedFormsOutput.forms",
            ),
            outputPath: "$.Payload.ExtractFormDataOutput",
            resultPath: "$.Payload.ExtractFormDataOutput",
          }).iterator(extractFormData),
        ),
        tracingEnabled: true,
      },
    );
  }
}
