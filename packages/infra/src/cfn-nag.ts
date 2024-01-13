// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { CfnResource, Stack } from "aws-cdk-lib";
import { NagSuppressions } from "cdk-nag";

const METADATA_TYPE = "cdk_nag";
const SUPRESSION_KEY = "rules_to_suppress";

export interface CfnNagRuleSuppression {
  id: string;
  reason: string;
}

/**
 * Adds cfn nag suppressions to the given construct
 */
export const addCfnNagSuppressions = (
  construct: CfnResource,
  rulesToSuppress: CfnNagRuleSuppression[],
): void => {
  construct.cfnOptions.metadata = {
    ...construct.cfnOptions.metadata,
    [METADATA_TYPE]: {
      ...construct.cfnOptions.metadata?.cdk_nag,
      [SUPRESSION_KEY]: [
        ...(construct.cfnOptions.metadata?.cdk_nag?.rules_to_suppress || []),
        ...rulesToSuppress,
      ],
    },
  };
};

/**
 * Adds cfn nag suppressions to the given stack
 */
export const addNagSupressionsToStack = (stack: Stack) => {
  NagSuppressions.addStackSuppressions(
    stack,
    [
      {
        id: "AwsSolutions-S1",
        reason: "overkill for this small sample",
      },
      {
        id: "AwsSolutions-IAM4",
        reason: "Managed policies are sufficient for a sample of this size",
      },
      {
        id: "AwsSolutions-IAM5",
        reason:
          "Some dynamic wildcard permissions are required for several service actions",
      },
      {
        id: "AwsSolutions-DDB3",
        reason: "Point in time recovery is not required",
      },
      {
        id: "AwsSolutions-L1",
        reason: "Lambda functions are using python 3.9",
      },
      {
        id: "AwsSolutions-SF1",
        reason:
          "Step functions not required to log ALL events. They are logged in lambda functions.",
      },
    ],
    true,
  );
};
