// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { PDKPipeline } from "@aws-prototyping-sdk/pipeline";
import { Stack, StackProps } from "aws-cdk-lib";
import { Construct } from "constructs";

/**
 * Defines the CI/CD pipeline
 */
export class PipelineStack extends Stack {
  readonly pipeline: PDKPipeline;

  constructor(scope: Construct, id: string, props: StackProps) {
    super(scope, id, props);

    this.pipeline = new PDKPipeline(this, "ApplicationPipeline", {
      primarySynthDirectory: "packages/infra/cdk.out",
      repositoryName: "monorepo",
      publishAssetsInParallel: false,
      crossAccountKeys: true,
      synth: {},
      synthShellStepPartialProps: {
        commands: ["npx projen && npx nx run @aws/infra:build"],
      },
    });
    this.pipeline.suppressCDKViolations();
  }
}
