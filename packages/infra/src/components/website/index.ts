// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { StaticWebsite } from "@aws/pdk/static-website";
import { CfnOutput, Stack } from "aws-cdk-lib";
import { Construct } from "constructs";
import { Auth } from "../auth/auth";
import { Source } from "../source";

export interface WebsiteProps {
  readonly authStack: Auth;
  readonly sourceStack: Source;
}

/**
 * Creates infrastructure components for a S3/Cloudfront React website
 */
export class Website extends Construct {
  constructor(scope: Construct, id: string, props: WebsiteProps) {
    super(scope, id);

    const website = new StaticWebsite(this, "Website", {
      websiteContentPath: "../webapp/build",
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

    new CfnOutput(this, "WebsiteUrl", {
      value: `https://${website.cloudFrontDistribution.distributionDomainName}/`,
    });
  }
}
