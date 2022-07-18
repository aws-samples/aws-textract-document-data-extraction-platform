// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { RemovalPolicy, Stack, StackProps } from "aws-cdk-lib";
import { UserPool } from "aws-cdk-lib/aws-cognito";
import { AttributeType } from "aws-cdk-lib/aws-dynamodb";
import {
  BlockPublicAccess,
  Bucket,
  BucketEncryption,
  HttpMethods,
} from "aws-cdk-lib/aws-s3";
import { Construct } from "constructs";
import { Table } from "../../common/dynamodb/table";
import { SourceApi } from "../api";
import { PopulateDefaultData } from "../defaults/populate-default-data";
import { DocumentIngestionStateMachine } from "../ingestion/document-ingestion-state-machine";

export interface SourceStackProps extends StackProps {
  readonly userPool: UserPool;
}

/**
 * Main stack for ingestion of source documents and extraction of their data
 */
export class SourceStack extends Stack {
  public readonly sourceApi: SourceApi;

  constructor(
    scope: Construct,
    id: string,
    { userPool, ...props }: SourceStackProps
  ) {
    super(scope, id, props);

    const sourceDocumentBucket = new Bucket(this, "SourceDocumentBucket", {
      enforceSSL: true,
      blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
      removalPolicy: RemovalPolicy.RETAIN,
      encryption: BucketEncryption.S3_MANAGED,
      // Cors required for get/put via presigned urls
      cors: [
        {
          allowedHeaders: ["*"],
          allowedOrigins: ["*"],
          allowedMethods: [HttpMethods.PUT, HttpMethods.GET, HttpMethods.POST],
        },
      ],
    });

    const formReviewWorkflowTagsTable = new Table(
      this,
      "FormReviewWorkflowTags",
      {
        partitionKey: {
          name: "tagId",
          type: AttributeType.STRING,
        },
        environmentVariableName: "FORM_REVIEW_WORKFLOW_TAGS_TABLE_NAME",
      }
    );

    const documentMetadataTable = new Table(this, "DocumentMetadata", {
      partitionKey: {
        name: "documentId",
        type: AttributeType.STRING,
      },
      environmentVariableName: "DOCUMENT_METADATA_TABLE_NAME",
    });

    const formMetadataTable = new Table(this, "FormMetadata", {
      partitionKey: {
        name: "documentId",
        type: AttributeType.STRING,
      },
      sortKey: {
        name: "formId",
        type: AttributeType.STRING,
      },
      environmentVariableName: "FORM_METADATA_TABLE_NAME",
    });

    const formSchemaTable = new Table(this, "FormSchemas", {
      partitionKey: {
        name: "schemaId",
        type: AttributeType.STRING,
      },
      environmentVariableName: "FORM_SCHEMA_TABLE_NAME",
    });

    const documentIngestionStateMachine = new DocumentIngestionStateMachine(
      this,
      "DocumentIngestionStateMachine",
      {
        sourceBucket: sourceDocumentBucket,
        documentMetadataTable,
        formMetadataTable,
        formSchemaTable,
      }
    );

    this.sourceApi = new SourceApi(this, "SourceApi", {
      userPool,
      sourceDocumentBucket,
      documentIngestionStateMachine,
      documentMetadataTable,
      formMetadataTable,
      formSchemaTable,
      formReviewWorkflowTagsTable,
    });

    new PopulateDefaultData(this, "PopulateDefaultData", {
      sourceApi: this.sourceApi,
    });
  }
}
