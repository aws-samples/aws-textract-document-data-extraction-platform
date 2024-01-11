// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { Duration } from "aws-cdk-lib";
import { Effect, PolicyStatement } from "aws-cdk-lib/aws-iam";
import { Bucket } from "aws-cdk-lib/aws-s3";
import {
  IntegrationPattern,
  JsonPath,
  StateMachine,
  TaskInput,
  TaskStateBase,
} from "aws-cdk-lib/aws-stepfunctions";
import {
  LambdaInvoke,
  StepFunctionsStartExecution,
} from "aws-cdk-lib/aws-stepfunctions-tasks";
import { Construct } from "constructs";
import { Table } from "../../common/dynamodb/table";
import {
  PythonLibLambda,
  PythonLibLambdaProps,
} from "../../common/lambda/python-lib-lambda";
import { grantPublishMetrics } from "../../common/metrics/permissions";
import { TextractStateMachine } from "../textract/textract-state-machine";

export interface FormIngestionStateMachineProps {
  readonly sourceBucket: Bucket;
  readonly documentMetadataTable: Table;
  readonly formMetadataTable: Table;
  readonly formSchemaTable: Table;
  readonly textractStateMachine: TextractStateMachine;
}

/**
 * State machine to orchestrate extraction of data from individual classified forms
 */
export class FormDataExtractionStateMachine extends Construct {
  public readonly stateMachine: StateMachine;

  constructor(
    scope: Construct,
    id: string,
    {
      textractStateMachine,
      documentMetadataTable,
      formMetadataTable,
      formSchemaTable,
      sourceBucket,
    }: FormIngestionStateMachineProps,
  ) {
    super(scope, id);

    const buildLambda = (
      handler: string,
      extraProps?: Omit<PythonLibLambdaProps, "handler">,
    ) =>
      new PythonLibLambda(this, handler, {
        handler: `form_data_extraction_state_machine/${handler}`,
        timeout: Duration.minutes(15),
        environment: {
          ...documentMetadataTable.environment,
          ...formMetadataTable.environment,
          ...formSchemaTable.environment,
        },
        ...extraProps,
      });

    const onErrorLambda = buildLambda("on_error");
    formMetadataTable.grantReadWriteData(onErrorLambda);
    grantPublishMetrics(onErrorLambda);

    const onError = new LambdaInvoke(this, "OnError", {
      lambdaFunction: onErrorLambda,
      payload: TaskInput.fromObject({
        payload: JsonPath.stringAt("$.Payload"),
        document_id: JsonPath.stringAt("$.Payload.Form.document_id"),
        form_id: JsonPath.stringAt("$.Payload.Form.form_id"),
        error_details: JsonPath.stringAt("$.ErrorDetails"),
      }),
      resultPath: JsonPath.DISCARD,
    });

    const withErrorHandler = (state: TaskStateBase) =>
      state.addCatch(onError, {
        resultPath: "$.ErrorDetails",
      });

    const startDataExtractionLambda = buildLambda("start_data_extraction");
    formMetadataTable.grantReadWriteData(startDataExtractionLambda);

    const startDataExtraction = withErrorHandler(
      new LambdaInvoke(this, "StartDataExtraction", {
        lambdaFunction: startDataExtractionLambda,
        payload: TaskInput.fromObject({
          form: JsonPath.stringAt("$.Payload.Form"),
          sfn_execution_arn: JsonPath.stringAt("$$.Execution.Id"),
        }),
        payloadResponseOnly: true,
        resultPath: "$.Payload.StartDataExtractionOutput",
      }),
    );

    const runTextract = withErrorHandler(
      new StepFunctionsStartExecution(this, "RunTextract", {
        stateMachine: textractStateMachine.stateMachine,
        input: TaskInput.fromObject({
          Payload: {
            DocumentLocation: JsonPath.stringAt("$.Payload.Form.location"),
            FeatureTypes: JsonPath.stringAt(
              "$.Payload.StartDataExtractionOutput.textract_feature_types",
            ),
            ExtraTextractArgs: JsonPath.stringAt(
              "$.Payload.StartDataExtractionOutput.textract_extra_args",
            ),
          },
        }),
        integrationPattern: IntegrationPattern.RUN_JOB,
        resultPath: "$.Payload.TextractOutput",
      }),
    );
    const extractFormDataLambda = buildLambda("extract_form_data");
    formMetadataTable.grantReadWriteData(extractFormDataLambda);
    documentMetadataTable.grantReadData(extractFormDataLambda);
    extractFormDataLambda.addToRolePolicy(
      new PolicyStatement({
        effect: Effect.ALLOW,
        actions: ["textract:GetDocumentAnalysis"],
        resources: ["*"],
      }),
    );
    sourceBucket.grantReadWrite(extractFormDataLambda);
    grantPublishMetrics(extractFormDataLambda);

    const extractFormData = withErrorHandler(
      new LambdaInvoke(this, "ExtractFormData", {
        lambdaFunction: extractFormDataLambda,
        payload: TaskInput.fromObject({
          form: JsonPath.stringAt("$.Payload.Form"),
          textract_job: JsonPath.stringAt("$.Payload.TextractOutput.Output"),
        }),
        payloadResponseOnly: true,
        resultPath: "$.Payload.ExtractFormDataOutput",
      }),
    );

    this.stateMachine = new StateMachine(this, "StateMachine", {
      definition: startDataExtraction.next(runTextract).next(extractFormData),
      tracingEnabled: true,
    });
  }
}
