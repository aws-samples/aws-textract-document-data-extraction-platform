// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import { PolicyStatement, Effect } from "aws-cdk-lib/aws-iam";
import {
  AwsCustomResource,
  AwsCustomResourcePolicy,
  PhysicalResourceId,
} from "aws-cdk-lib/custom-resources";
import { Construct } from "constructs";
import { ApiExtended } from "../../../constructs/api-extended";
import { SourceApi } from "../api";
import { APPENDIX_3X } from "./form-schemas/appendix-3x";
import { APPENDIX_3Y } from "./form-schemas/appendix-3y";
import { APPENDIX_3Z } from "./form-schemas/appendix-3z";
import { REVIEW_WORKFLOW_TAGS } from "./review-workflow-tags/tags";

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
    { sourceApi }: PopulateDefaultDataProps
  ) {
    super(scope, id);

    this.defaultFormSchemas(sourceApi.api);
    this.defaultFormReviewWorkflowTags(sourceApi.api);
  }

  private defaultFormSchemas = (api: ApiExtended) => {
    [APPENDIX_3X, APPENDIX_3Y, APPENDIX_3Z].forEach((schema) => {
      new AwsCustomResource(
        this,
        `default21Schema${schema.title.replace(/\s/g, "")}`,
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
              FunctionName:
                api.integrations.createFormSchema.function.functionArn,
              Payload: JSON.stringify({
                pathParameters: {},
                queryStringParameters: {},
                multiValueQueryStringParameters: {},
                body: schema ? JSON.stringify(schema) : "",
                headers: DEFAULT_HEADERS,
              }),
            },
            physicalResourceId: PhysicalResourceId.of(
              `CreateDefaultSchema${schema.title.replace(/\s/g, "")}`
            ),
            outputPaths: ["status"],
          },
        }
      );
    });
  };
  // private defaultFormSchemas = (api: Api) => {
  //   [APPENDIX_3X, APPENDIX_3Y, APPENDIX_3Z].forEach((schema) => {
  //     api.invokeLambdaFor(
  //       "createFormSchema",
  //       `CreateDefaultSchema${schema.title.replace(/\s/g, "")}`,
  //       {
  //         requestParameters: {},
  //         requestArrayParameters: {},
  //         body: schema,
  //       },
  //       DEFAULT_HEADERS
  //     );
  //   });
  // };

  private defaultFormReviewWorkflowTags = (api: ApiExtended) => {
    REVIEW_WORKFLOW_TAGS.forEach((tag) => {
      new AwsCustomResource(
        this,
        `default21FormReviewWorkflowTag${tag.tagText.replace(/\s/g, "")}`,
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
              FunctionName:
                api.integrations.createFormReviewWorkflowTag.function
                  .functionArn,
              Payload: JSON.stringify({
                pathParameters: {},
                queryStringParameters: {},
                multiValueQueryStringParameters: {},
                body: tag ? JSON.stringify(tag) : "",
                headers: DEFAULT_HEADERS,
              }),
            },
            physicalResourceId: PhysicalResourceId.of(
              `CreateFormReviewWorkflowTag${tag.tagText.replace(/\s/g, "")}`
            ),
            outputPaths: ["status"],
          },
        }
      );
    });
  };
}
