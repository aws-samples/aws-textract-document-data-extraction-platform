// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { StaticWebsite } from "@aws/pdk/static-website";
import { CfnOutput, NestedStack, NestedStackProps, Stack } from "aws-cdk-lib";
import { Construct } from "constructs";
import { AuthStack } from "../auth/auth-stack";
import { SourceStack } from "../source/stack";

export interface WebsiteStackProps extends NestedStackProps {
  readonly authStack: AuthStack;
  readonly sourceStack: SourceStack;
}

/**
 * Creates infrastructure components for a S3/Cloudfront React website
 */
export class WebsiteStack extends NestedStack {
  constructor(scope: Construct, id: string, props: WebsiteStackProps) {
    super(scope, id, props);

    const website = new StaticWebsite(this, id, {
      websiteContentPath: "../website/build",
      runtimeOptions: {
        jsonPayload: {
          region: Stack.of(this).region,
          identityPoolId: props.authStack.identityPool.ref,
          userPoolId: props.authStack.userPool.userPoolId,
          userPoolWebClientId: props.authStack.userPoolClient.userPoolClientId,
          sourceApiUrl: props?.sourceStack.sourceApi.api.api.urlForPath(),
        },
      },
    });

    new CfnOutput(this, "DistributionDomainName", {
      exportName: "DistributionDomainName",
      value: website.cloudFrontDistribution.distributionDomainName,
    });
  }
}
