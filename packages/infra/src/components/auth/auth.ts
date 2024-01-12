// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { Duration } from "aws-cdk-lib";
import {
  CfnIdentityPool,
  CfnUserPool,
  UserPool,
  UserPoolClient,
} from "aws-cdk-lib/aws-cognito";
import { Construct } from "constructs";

export interface AuthProps {}

/**
 * Creates Cognito resources for auth
 */
export class Auth extends Construct {
  public readonly userPool: UserPool;
  public readonly identityPool: CfnIdentityPool;
  public readonly userPoolClient: UserPoolClient;

  constructor(scope: Construct, id: string, _props?: AuthProps) {
    super(scope, id);

    this.userPool = new UserPool(this, "UserPool", {
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

    // this.userPoolDomain = new UserPoolDomain(this, "UserPoolDomain", {
    //   userPool: this.userPool,
    //   cognitoDomain: {
    //     domainPrefix: `${Stack.of(this).account}`,
    //   },
    // });

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
