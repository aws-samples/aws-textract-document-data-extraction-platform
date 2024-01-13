// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { Stack, StackProps } from "aws-cdk-lib";
import { Construct } from "constructs";
import { addNagSupressionsToStack } from "../cfn-nag";
import { Auth } from "../components/auth/auth";
import { Permissions } from "../components/auth/permissions";
import { Source } from "../components/source";
import { Website } from "../components/website";

export class ApplicationStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const authStack = new Auth(this, "AuthStack", {});
    const sourceStack = new Source(this, "SourceStack", {
      userPool: authStack.userPool,
    });
    new Website(this, "WebsiteStack", {
      authStack,
      sourceStack,
    });
    new Permissions(this, "PermissionsStack", {
      userPool: authStack.userPool,
      identityPool: authStack.identityPool,
      sourceApi: sourceStack.sourceApi,
    });

    addNagSupressionsToStack(this);
  }
}
