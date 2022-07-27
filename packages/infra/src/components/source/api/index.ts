// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { Authorizers } from "@aws-prototyping-sdk/open-api-gateway";
import { Stack } from "aws-cdk-lib";
import { Cors } from "aws-cdk-lib/aws-apigateway";
import { UserPool } from "aws-cdk-lib/aws-cognito";
import {
  AccountPrincipal,
  AnyPrincipal,
  Effect,
  PolicyDocument,
  PolicyStatement,
} from "aws-cdk-lib/aws-iam";
import { Bucket } from "aws-cdk-lib/aws-s3";
import { Construct } from "constructs";
import { ApiExtended } from "../../../constructs/api-extended";
import { Table } from "../../common/dynamodb/table";
import { PythonLambda } from "../../common/lambda/python-lambda";
import {
  grantPublishMetrics,
  grantReadMetrics,
} from "../../common/metrics/permissions";
import { DocumentIngestionStateMachine } from "../ingestion/document-ingestion-state-machine";

export interface SourceApiProps {
  readonly userPool: UserPool;
  readonly sourceDocumentBucket: Bucket;
  readonly documentIngestionStateMachine: DocumentIngestionStateMachine;
  readonly documentMetadataTable: Table;
  readonly formMetadataTable: Table;
  readonly formSchemaTable: Table;
  readonly formReviewWorkflowTagsTable: Table;
}

/**
 * Construct defining the API methods and integrations
 */
export class SourceApi extends Construct {
  public readonly api: ApiExtended;

  constructor(
    scope: Construct,
    id: string,
    {
      userPool,
      sourceDocumentBucket,
      documentIngestionStateMachine,
      documentMetadataTable,
      formMetadataTable,
      formSchemaTable,
      formReviewWorkflowTagsTable,
    }: SourceApiProps
  ) {
    super(scope, id);

    const buildLambda = (handler: string) => {
      const lambda = new PythonLambda(this, handler, {
        handler: `api/${handler}`,
        environment: {
          SOURCE_DOCUMENT_BUCKET: sourceDocumentBucket.bucketName,
          DOCUMENT_INGESTION_STATE_MACHINE_ARN:
            documentIngestionStateMachine.stateMachine.stateMachineArn,
          ...documentMetadataTable.environment,
          ...formMetadataTable.environment,
          ...formSchemaTable.environment,
          ...formReviewWorkflowTagsTable.environment,
        },
      });
      // Grant all lambdas permissions to list users in the user pool for the generic api wrapper to look up any
      // callers authenticated via cognito
      lambda.addToRolePolicy(
        new PolicyStatement({
          effect: Effect.ALLOW,
          actions: ["cognito-idp:ListUsers"],
          resources: [userPool.userPoolArn],
        })
      );
      return lambda;
    };

    const createFormReviewWorkflowTagLambda = buildLambda(
      "form_review_workflow_tags/create_form_review_workflow_tag"
    );
    formReviewWorkflowTagsTable.grantReadWriteData(
      createFormReviewWorkflowTagLambda
    );

    const listFormReviewWorkflowTagsLambda = buildLambda(
      "form_review_workflow_tags/list_form_review_workflow_tags"
    );
    formReviewWorkflowTagsTable.grantReadData(listFormReviewWorkflowTagsLambda);

    const getDocumentUploadUrlLambda = buildLambda("get_document_upload_url");
    sourceDocumentBucket.grantReadWrite(getDocumentUploadUrlLambda);

    const submitSourceDocumentLambda = buildLambda("submit_source_document");

    sourceDocumentBucket.grantReadWrite(submitSourceDocumentLambda);
    documentIngestionStateMachine.stateMachine.grantStartExecution(
      submitSourceDocumentLambda
    );
    documentMetadataTable.grantReadWriteData(submitSourceDocumentLambda);

    const getDocumentLambda = buildLambda("get_document");
    documentMetadataTable.grantReadData(getDocumentLambda);
    sourceDocumentBucket.grantRead(getDocumentLambda);

    const listDocumentsLambda = buildLambda("list_documents");
    documentMetadataTable.grantReadData(listDocumentsLambda);

    const listDocumentFormsLambda = buildLambda("list_document_forms");
    documentMetadataTable.grantReadData(listDocumentFormsLambda);
    formMetadataTable.grantReadData(listDocumentFormsLambda);

    const listFormsLambda = buildLambda("list_forms");
    formMetadataTable.grantReadData(listFormsLambda);

    const getDocumentFormLambda = buildLambda("get_document_form");
    formMetadataTable.grantReadData(getDocumentFormLambda);
    sourceDocumentBucket.grantRead(getDocumentFormLambda);

    const createFormSchemaLambda = buildLambda(
      "form_schema/create_form_schema"
    );
    formSchemaTable.grantReadWriteData(createFormSchemaLambda);

    const updateFormSchemaLambda = buildLambda(
      "form_schema/update_form_schema"
    );
    formSchemaTable.grantReadWriteData(updateFormSchemaLambda);

    const deleteFormSchemaLambda = buildLambda(
      "form_schema/delete_form_schema"
    );
    formSchemaTable.grantReadWriteData(deleteFormSchemaLambda);

    const getFormSchemaLambda = buildLambda("form_schema/get_form_schema");
    formSchemaTable.grantReadData(getFormSchemaLambda);

    const listFormSchemasLambda = buildLambda("form_schema/list_form_schemas");
    formSchemaTable.grantReadData(listFormSchemasLambda);

    const updateFormReviewLambda = buildLambda(
      "form_review/update_form_review"
    );
    formMetadataTable.grantReadWriteData(updateFormReviewLambda);

    const updateStatusLambda = buildLambda("form_review/update_status");
    formMetadataTable.grantReadWriteData(updateStatusLambda);
    documentMetadataTable.grantReadData(updateStatusLambda);
    grantPublishMetrics(updateStatusLambda);

    const getMetricsLambda = buildLambda("metrics/get_metrics");
    formSchemaTable.grantReadData(getMetricsLambda);
    grantReadMetrics(getMetricsLambda);

    this.api = new ApiExtended(this, "Api", {
      defaultAuthorizer: Authorizers.iam(),
      corsOptions: {
        allowOrigins: Cors.ALL_ORIGINS,
        allowHeaders: [
          ...Cors.DEFAULT_HEADERS,
          "x-username",
          "x-amz-content-sha256",
          "x-filename",
        ],
      },
      integrations: {
        createFormReviewWorkflowTag: {
          function: createFormReviewWorkflowTagLambda,
        },
        listFormReviewWorkflowTags: {
          function: listFormReviewWorkflowTagsLambda,
        },
        getDocumentUploadUrl: {
          function: getDocumentUploadUrlLambda,
        },
        submitSourceDocument: {
          function: submitSourceDocumentLambda,
        },
        getDocument: {
          function: getDocumentLambda,
        },
        listDocuments: {
          function: listDocumentsLambda,
        },
        listDocumentForms: {
          function: listDocumentFormsLambda,
        },
        listForms: {
          function: listFormsLambda,
        },
        getDocumentForm: {
          function: getDocumentFormLambda,
        },
        createFormSchema: {
          function: createFormSchemaLambda,
        },
        updateFormSchema: {
          function: updateFormSchemaLambda,
        },
        deleteFormSchema: {
          function: deleteFormSchemaLambda,
        },
        getFormSchema: {
          function: getFormSchemaLambda,
        },
        listFormSchemas: {
          function: listFormSchemasLambda,
        },
        updateFormReview: {
          function: updateFormReviewLambda,
        },
        updateStatus: {
          function: updateStatusLambda,
        },
        getMetrics: {
          function: getMetricsLambda,
        },
      },
      policy: new PolicyDocument({
        statements: [
          // Here we grant any AWS credentials from the account that the prototype is deployed in to call the api.
          // Machine to machine fine-grained access can be defined here using more specific principals (eg roles or
          // users) and resources (ie which api paths may be invoked by which principal) if required.
          new PolicyStatement({
            effect: Effect.ALLOW,
            principals: [new AccountPrincipal(Stack.of(this).account)],
            actions: ["execute-api:Invoke"],
            resources: ["execute-api:/*"],
          }),
          // Open up OPTIONS to allow browsers to make unauthenticated preflight requests
          new PolicyStatement({
            effect: Effect.ALLOW,
            principals: [new AnyPrincipal()],
            actions: ["execute-api:Invoke"],
            resources: ["execute-api:/*/OPTIONS/*"],
          }),
        ],
      }),
    });
  }
}
