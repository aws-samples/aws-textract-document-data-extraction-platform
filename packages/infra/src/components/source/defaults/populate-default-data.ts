// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { PolicyStatement, Effect } from "aws-cdk-lib/aws-iam";
import {
  AwsCustomResource,
  AwsCustomResourcePolicy,
  PhysicalResourceId,
} from "aws-cdk-lib/custom-resources";
import { Construct } from "constructs";
import { W_8BEN } from "./form-schemas/w-8ben";
import { REVIEW_WORKFLOW_TAGS } from "./review-workflow-tags/tags";
import { SourceApi } from "../api";

export interface PopulateDefaultDataProps {
  readonly sourceApi: SourceApi;
}

const DEFAULT_HEADERS = {
  "x-username": "system",
};

/**
 * Populates any default data by invoking apis during deployment
 */
export class PopulateDefaultData extends Construct {
  constructor(
    scope: Construct,
    id: string,
    { sourceApi }: PopulateDefaultDataProps,
  ) {
    super(scope, id);

    this.defaultFormSchemas(sourceApi);
    this.defaultFormReviewWorkflowTags(sourceApi);
  }

  private defaultFormSchemas = (api: SourceApi) => {
    [W_8BEN].forEach((schema) => {
      new AwsCustomResource(
        this,
        `DefaultSchema${schema.title.replace(/\s/g, "")}`,
        {
          policy: AwsCustomResourcePolicy.fromStatements([
            new PolicyStatement({
              effect: Effect.ALLOW,
              actions: ["lambda:InvokeFunction"],
              resources: ["*"],
            }),
          ]),
          onUpdate: {
            service: "Lambda",
            action: "invoke",
            parameters: {
              FunctionName: api.createFormSchema.functionArn,
              Payload: JSON.stringify({
                pathParameters: {},
                queryStringParameters: {},
                multiValueQueryStringParameters: {},
                body: schema ? JSON.stringify(schema) : "",
                headers: DEFAULT_HEADERS,
              }),
            },
            physicalResourceId: PhysicalResourceId.of(
              `CreateDefaultSchema${schema.title.replace(/\s/g, "")}`,
            ),
            outputPaths: ["status"],
          },
        },
      );
    });
  };

  private defaultFormReviewWorkflowTags = (api: SourceApi) => {
    REVIEW_WORKFLOW_TAGS.forEach((tag) => {
      new AwsCustomResource(
        this,
        `DefaultFormReviewTag${tag.tagText.replace(/\s/g, "")}`,
        {
          policy: AwsCustomResourcePolicy.fromStatements([
            new PolicyStatement({
              effect: Effect.ALLOW,
              actions: ["lambda:InvokeFunction"],
              resources: ["*"],
            }),
          ]),
          onUpdate: {
            service: "Lambda",
            action: "invoke",
            parameters: {
              FunctionName: api.createFormReviewWorkflowTag.functionArn,
              Payload: JSON.stringify({
                pathParameters: {},
                queryStringParameters: {},
                multiValueQueryStringParameters: {},
                body: tag ? JSON.stringify(tag) : "",
                headers: DEFAULT_HEADERS,
              }),
            },
            physicalResourceId: PhysicalResourceId.of(
              `CreateFormReviewWorkflowTag${tag.tagText.replace(/\s/g, "")}`,
            ),
            outputPaths: ["status"],
          },
        },
      );
    });
  };
}
