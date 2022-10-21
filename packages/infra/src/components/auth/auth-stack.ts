// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import {
  Duration,
  Stack,
  StackProps,
  aws_apigateway as apigateway,
} from "aws-cdk-lib";
import {
  CfnIdentityPool,
  CfnUserPool,
  UserPool,
  UserPoolClient,
  UserPoolDomain,
} from "aws-cdk-lib/aws-cognito";
import * as iam from "aws-cdk-lib/aws-iam";
import { Construct } from "constructs";

export interface AuthStackProps extends StackProps {}

/**
 * Creates Cognito resources for auth
 */
export class AuthStack extends Stack {
  public readonly userPool: UserPool;
  public readonly identityPool: CfnIdentityPool;
  public readonly userPoolDomain: UserPoolDomain;
  public readonly userPoolClient: UserPoolClient;

  constructor(scope: Construct, id: string, props: AuthStackProps) {
    super(scope, id, props);

    const cloudWatchRole = new iam.Role(this, "app_cloudwatchrole", {
      assumedBy: new iam.CompositePrincipal(
        new iam.ServicePrincipal("apigateway.amazonaws.com")
      ),
      roleName: "app_cloudwatchrole",
    });

    // this is to get around weird CDK deployment issues where the
    // apigw resource deployment fails due to the absence of the
    // account cw logs role being set

    cloudWatchRole.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName(
        "service-role/AmazonAPIGatewayPushToCloudWatchLogs"
      )
    );

    new apigateway.CfnAccount(this, "account", {
      cloudWatchRoleArn: cloudWatchRole.roleArn,
    });

    this.userPool = new UserPool(this, "UserPool", {
      userPoolName: "UserPool",
      selfSignUpEnabled: false,
      signInAliases: {
        username: true,
      },
      standardAttributes: {
        givenName: {
          required: true,
          mutable: true,
        },
        familyName: {
          required: true,
          mutable: true,
        },
        email: {
          required: true,
          mutable: true,
        },
      },
      passwordPolicy: {
        minLength: 8,
        requireDigits: true,
        requireLowercase: true,
        requireSymbols: true,
        requireUppercase: true,
        tempPasswordValidity: Duration.days(7),
      },
    });

    const cfnUserPool = this.userPool.node.defaultChild as CfnUserPool;
    cfnUserPool.userPoolAddOns = {
      advancedSecurityMode: "ENFORCED",
    };

    this.userPoolDomain = new UserPoolDomain(this, "UserPoolDomain", {
      userPool: this.userPool,
      cognitoDomain: {
        domainPrefix: `${this.account}`,
      },
    });

    this.userPoolClient = this.userPool.addClient("UserPoolClient", {
      authFlows: {
        adminUserPassword: true,
        userPassword: true,
        userSrp: true,
        custom: true,
      },
      generateSecret: false,
    });

    // Cognito identity pool
    this.identityPool = new CfnIdentityPool(this, "IdentityPool", {
      allowUnauthenticatedIdentities: false,
      cognitoIdentityProviders: [
        {
          clientId: this.userPoolClient.userPoolClientId,
          providerName: this.userPool.userPoolProviderName,
        },
      ],
    });
  }
}
