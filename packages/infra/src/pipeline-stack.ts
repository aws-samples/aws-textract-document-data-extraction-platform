// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { Stack, StackProps } from "aws-cdk-lib";
import { pipeline } from "aws-prototyping-sdk";
import { Construct } from "constructs";

/**
 * Defines the CI/CD pipeline
 */
export class PipelineStack extends Stack {
  readonly pipeline: pipeline.PDKPipeline;

  constructor(scope: Construct, id: string, props: StackProps) {
    super(scope, id, props);

    this.pipeline = new pipeline.PDKPipeline(this, "ApplicationPipeline", {
      primarySynthDirectory: "packages/infra/cdk.out",
      repositoryName: "monorepo",
      publishAssetsInParallel: false,
      crossAccountKeys: true,
      synth: {},
      synthShellStepPartialProps: {
        commands: ["npx projen && npx nx run @aws/infra:build"],
      },
      // Optional: if you use SonarQube, you can provide config to execute a code scan here
      sonarCodeScannerConfig: this.node.tryGetContext("sonarqubeScannerConfig"),
    });
  }
}
