// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import * as path from "path";
import { CustomResource, Stage, StageProps, Duration } from "aws-cdk-lib";
import { Effect, PolicyStatement } from "aws-cdk-lib/aws-iam";
import { Function, Code, Runtime } from "aws-cdk-lib/aws-lambda";
import { Bucket } from "aws-cdk-lib/aws-s3";
import { BucketDeployment } from "aws-cdk-lib/aws-s3-deployment";
import { Provider } from "aws-cdk-lib/custom-resources";
import { Construct } from "constructs";
import { addNagSupressionsToStack } from "./cfn-nag";
import { AuthStack } from "./components/auth/auth-stack";
import { PermissionsStack } from "./components/auth/permissions-stack";
import { SourceStack } from "./components/source/stack";
import { WebsiteStack } from "./components/website";

export interface ApplicationStageProps extends StageProps {}

export class ApplicationStage extends Stage {
  constructor(scope: Construct, id: string, props: ApplicationStageProps) {
    super(scope, id, props);

    const authStack = new AuthStack(this, "AuthStack", {});
    const sourceStack = new SourceStack(this, "SourceStack", {
      userPool: authStack.userPool,
    });
    const websiteStack = new WebsiteStack(this, "WebsiteStack", {});
    const permissionsStack = new PermissionsStack(this, "PermissionsStack", {
      userPool: authStack.userPool,
      identityPool: authStack.identityPool,
      sourceApi: sourceStack.sourceApi,
    });

    // Configuration to be dynamically loaded by the website, allowing it to "point" to the deployed resources
    const websiteConfiguration: string = `window['runtimeConfig'] = {
      "region": "${websiteStack.region}",
      "userPoolId": "${authStack.userPool.userPoolId}",
      "userPoolWebClientId": "${authStack.userPoolClient.userPoolClientId}",
      "identityPoolId": "${authStack.identityPool.ref}",
      "sourceApiUrl": "${sourceStack.sourceApi.api.api.urlForPath()}",
    };`;

    uploadWebsiteConfig(
      {
        bucket: websiteStack.websiteBucket,
        configFilename: "runtime-configuration.js",
        distributionId: websiteStack.distribution.distributionId,
        websiteConfiguration: websiteConfiguration,
        bucketDeployment: websiteStack.bucketDeployment,
      },
      websiteStack
    );
    const stacks = [sourceStack, authStack, websiteStack, permissionsStack];
    stacks.forEach((stack) => addNagSupressionsToStack(stack));
  }
}

export interface WebsiteConfigProps {
  bucket: Bucket;
  configFilename: string;
  distributionId: string;
  websiteConfiguration: string;
  bucketDeployment: BucketDeployment;
}

/**
 * Upload the website config to s3 via a custom resource
 */
const uploadWebsiteConfig = (props: WebsiteConfigProps, scope: Construct) => {
  const uploadWebsiteConfigFunction: Function = new Function(
    scope,
    "AppUploadWebsiteConfigFunction",
    {
      runtime: Runtime.PYTHON_3_9,
      timeout: Duration.seconds(60),
      handler: "app.on_event",
      code: Code.fromAsset(
        path.join(__dirname, "../custom-resources/upload-website-config")
      ),
      initialPolicy: [
        new PolicyStatement({
          effect: Effect.ALLOW,
          actions: [
            "cloudfront:GetInvalidation",
            "cloudfront:CreateInvalidation",
          ],
          resources: ["*"],
        }),
      ],
    }
  );

  props.bucket.grantWrite(uploadWebsiteConfigFunction);

  const uploadWebsiteConfigProvider: Provider = new Provider(
    scope,
    "AppUploadWebsiteConfigProvider",
    {
      onEventHandler: uploadWebsiteConfigFunction,
    }
  );

  const uploadWebsiteConfigResource: CustomResource = new CustomResource(
    scope,
    "AppUploadWebsiteConfigResource",
    {
      serviceToken: uploadWebsiteConfigProvider.serviceToken,
      properties: {
        S3_BUCKET: props.bucket.bucketName,
        S3_CONFIG_FILE_KEY: "runtime-configuration.js",
        WEBSITE_CONFIG: props.websiteConfiguration,
        CLOUDFRONT_DISTRIBUTION_ID: props.distributionId,
        // Ensure we always write the config, since deployment of website updates will clear the s3 bucket.
        ALWAYS_UPDATE: new Date().toISOString(),
      },
    }
  );

  uploadWebsiteConfigResource.node.addDependency(props.bucketDeployment);
};
