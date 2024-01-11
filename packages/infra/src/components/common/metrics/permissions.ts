// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { Effect, PolicyStatement } from "aws-cdk-lib/aws-iam";
import { Function as LambdaFunction } from "aws-cdk-lib/aws-lambda";

const METRICS_NAMESPACE = "aws/disclosure-data-extraction";

/**
 * Grants the given lambda function permissions to publish metrics
 */
export const grantPublishMetrics = (lambda: LambdaFunction) =>
  lambda.addToRolePolicy(
    new PolicyStatement({
      effect: Effect.ALLOW,
      actions: ["cloudwatch:PutMetricData"],
      resources: ["*"],
      conditions: {
        StringEquals: {
          "cloudwatch:namespace": METRICS_NAMESPACE,
        },
      },
    }),
  );

/**
 * Grants the given lambda function permissions to read metrics
 */
export const grantReadMetrics = (lambda: LambdaFunction) =>
  lambda.addToRolePolicy(
    new PolicyStatement({
      effect: Effect.ALLOW,
      actions: ["cloudwatch:GetMetricStatistics"],
      resources: ["*"],
    }),
  );
