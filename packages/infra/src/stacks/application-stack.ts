import { Stack, StackProps } from "aws-cdk-lib";
import { Construct } from "constructs";
import { addNagSupressionsToStack } from "../cfn-nag";
import { AuthStack } from "../components/auth/auth-stack";
import { PermissionsStack } from "../components/auth/permissions-stack";
import { SourceStack } from "../components/source/stack";
import { WebsiteStack } from "../components/website";

export class ApplicationStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const authStack = new AuthStack(this, "AuthStack", {});
    const sourceStack = new SourceStack(this, "SourceStack", {
      userPool: authStack.userPool,
    });
    new WebsiteStack(this, "WebsiteStack", {
      authStack,
      sourceStack,
    });
    new PermissionsStack(this, "PermissionsStack", {
      userPool: authStack.userPool,
      identityPool: authStack.identityPool,
      sourceApi: sourceStack.sourceApi,
    });

    addNagSupressionsToStack(this);
  }
}
