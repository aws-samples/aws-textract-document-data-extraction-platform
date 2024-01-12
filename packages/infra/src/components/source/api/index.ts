// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import {
  Api,
  CreateFormReviewWorkflowTagFunction,
  CreateFormSchemaFunction,
  DeleteFormSchemaFunction,
  GetDocumentFormFunction,
  GetDocumentFunction,
  GetDocumentUploadUrlFunction,
  GetFormSchemaFunction,
  GetMetricsFunction,
  ListDocumentFormsFunction,
  ListDocumentsFunction,
  ListFormReviewWorkflowTagsFunction,
  ListFormSchemasFunction,
  ListFormsFunction,
  SubmitSourceDocumentFunction,
  UpdateFormReviewFunction,
  UpdateFormSchemaFunction,
  UpdateStatusFunction,
} from "@aws/document-extraction-platform-api-typescript-infra";
import { Authorizers, Integrations } from "@aws/pdk/type-safe-api";
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
import { FunctionProps, IFunction } from "aws-cdk-lib/aws-lambda";
import { Bucket } from "aws-cdk-lib/aws-s3";
import { Construct } from "constructs";
import { Table } from "../../common/dynamodb/table";
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
  public readonly api: Api;

  public readonly createFormSchema: IFunction;
  public readonly createFormReviewWorkflowTag: IFunction;

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
    }: SourceApiProps,
  ) {
    super(scope, id);

    const apiLambdaProps = {
      environment: {
        SOURCE_DOCUMENT_BUCKET: sourceDocumentBucket.bucketName,
        DOCUMENT_INGESTION_STATE_MACHINE_ARN:
          documentIngestionStateMachine.stateMachine.stateMachineArn,
        ...documentMetadataTable.environment,
        ...formMetadataTable.environment,
        ...formSchemaTable.environment,
        ...formReviewWorkflowTagsTable.environment,
      },
      initialPolicy: [
        // Grant all lambdas permissions to list users in the user pool for the generic api wrapper to look up any
        // callers authenticated via cognito
        new PolicyStatement({
          effect: Effect.ALLOW,
          actions: ["cognito-idp:ListUsers"],
          resources: [userPool.userPoolArn],
        }),
      ],
      memorySize: 256,
    } satisfies Partial<FunctionProps>;

    const createFormReviewWorkflowTagLambda =
      new CreateFormReviewWorkflowTagFunction(
        this,
        "CreateFormReviewWorkflowTag",
        apiLambdaProps,
      );
    this.createFormReviewWorkflowTag = createFormReviewWorkflowTagLambda;
    formReviewWorkflowTagsTable.grantReadWriteData(
      createFormReviewWorkflowTagLambda,
    );

    const listFormReviewWorkflowTagsLambda =
      new ListFormReviewWorkflowTagsFunction(
        this,
        "listFormReviewWorkflowTags",
        apiLambdaProps,
      );
    formReviewWorkflowTagsTable.grantReadData(listFormReviewWorkflowTagsLambda);

    const getDocumentUploadUrlLambda = new GetDocumentUploadUrlFunction(
      this,
      "GetDocumentUploadUrl",
      apiLambdaProps,
    );
    sourceDocumentBucket.grantReadWrite(getDocumentUploadUrlLambda);

    const submitSourceDocumentLambda = new SubmitSourceDocumentFunction(
      this,
      "SubmitSourceDocument",
      apiLambdaProps,
    );

    sourceDocumentBucket.grantReadWrite(submitSourceDocumentLambda);
    documentIngestionStateMachine.stateMachine.grantStartExecution(
      submitSourceDocumentLambda,
    );
    documentMetadataTable.grantReadWriteData(submitSourceDocumentLambda);

    const getDocumentLambda = new GetDocumentFunction(
      this,
      "GetDocument",
      apiLambdaProps,
    );
    documentMetadataTable.grantReadData(getDocumentLambda);
    sourceDocumentBucket.grantRead(getDocumentLambda);

    const listDocumentsLambda = new ListDocumentsFunction(
      this,
      "ListDocuments",
      apiLambdaProps,
    );
    documentMetadataTable.grantReadData(listDocumentsLambda);

    const listDocumentFormsLambda = new ListDocumentFormsFunction(
      this,
      "ListDocumentForms",
      apiLambdaProps,
    );
    documentMetadataTable.grantReadData(listDocumentFormsLambda);
    formMetadataTable.grantReadData(listDocumentFormsLambda);

    const listFormsLambda = new ListFormsFunction(
      this,
      "ListForms",
      apiLambdaProps,
    );
    formMetadataTable.grantReadData(listFormsLambda);

    const getDocumentFormLambda = new GetDocumentFormFunction(
      this,
      "GetDocumentForm",
      apiLambdaProps,
    );
    formMetadataTable.grantReadData(getDocumentFormLambda);
    sourceDocumentBucket.grantRead(getDocumentFormLambda);

    const createFormSchemaLambda = new CreateFormSchemaFunction(
      this,
      "CreateFormSchema",
      apiLambdaProps,
    );
    this.createFormSchema = createFormSchemaLambda;
    formSchemaTable.grantReadWriteData(createFormSchemaLambda);

    const updateFormSchemaLambda = new UpdateFormSchemaFunction(
      this,
      "UpdateFormSchema",
      apiLambdaProps,
    );
    formSchemaTable.grantReadWriteData(updateFormSchemaLambda);

    const deleteFormSchemaLambda = new DeleteFormSchemaFunction(
      this,
      "DeleteFormSchema",
      apiLambdaProps,
    );
    formSchemaTable.grantReadWriteData(deleteFormSchemaLambda);

    const getFormSchemaLambda = new GetFormSchemaFunction(
      this,
      "GetFormSchema",
      apiLambdaProps,
    );
    formSchemaTable.grantReadData(getFormSchemaLambda);

    const listFormSchemasLambda = new ListFormSchemasFunction(
      this,
      "ListFormSchemas",
      apiLambdaProps,
    );
    formSchemaTable.grantReadData(listFormSchemasLambda);

    const updateFormReviewLambda = new UpdateFormReviewFunction(
      this,
      "UpdateFormReview",
      apiLambdaProps,
    );
    formMetadataTable.grantReadWriteData(updateFormReviewLambda);

    const updateStatusLambda = new UpdateStatusFunction(
      this,
      "UpdateStatus",
      apiLambdaProps,
    );
    formMetadataTable.grantReadWriteData(updateStatusLambda);
    documentMetadataTable.grantReadData(updateStatusLambda);
    grantPublishMetrics(updateStatusLambda);

    const getMetricsLambda = new GetMetricsFunction(
      this,
      "GetMetrics",
      apiLambdaProps,
    );
    formSchemaTable.grantReadData(getMetricsLambda);
    grantReadMetrics(getMetricsLambda);

    this.api = new Api(this, "Api", {
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
          integration: Integrations.lambda(createFormReviewWorkflowTagLambda),
        },
        listFormReviewWorkflowTags: {
          integration: Integrations.lambda(listFormReviewWorkflowTagsLambda),
        },
        getDocumentUploadUrl: {
          integration: Integrations.lambda(getDocumentUploadUrlLambda),
        },
        submitSourceDocument: {
          integration: Integrations.lambda(submitSourceDocumentLambda),
        },
        getDocument: {
          integration: Integrations.lambda(getDocumentLambda),
        },
        listDocuments: {
          integration: Integrations.lambda(listDocumentsLambda),
        },
        listDocumentForms: {
          integration: Integrations.lambda(listDocumentFormsLambda),
        },
        listForms: {
          integration: Integrations.lambda(listFormsLambda),
        },
        getDocumentForm: {
          integration: Integrations.lambda(getDocumentFormLambda),
        },
        createFormSchema: {
          integration: Integrations.lambda(createFormSchemaLambda),
        },
        updateFormSchema: {
          integration: Integrations.lambda(updateFormSchemaLambda),
        },
        deleteFormSchema: {
          integration: Integrations.lambda(deleteFormSchemaLambda),
        },
        getFormSchema: {
          integration: Integrations.lambda(getFormSchemaLambda),
        },
        listFormSchemas: {
          integration: Integrations.lambda(listFormSchemasLambda),
        },
        updateFormReview: {
          integration: Integrations.lambda(updateFormReviewLambda),
        },
        updateStatus: {
          integration: Integrations.lambda(updateStatusLambda),
        },
        getMetrics: {
          integration: Integrations.lambda(getMetricsLambda),
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
