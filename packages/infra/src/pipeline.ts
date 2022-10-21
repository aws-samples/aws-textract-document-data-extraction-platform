// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import { PDKNag } from "aws-prototyping-sdk/pdk-nag";
import { ApplicationStage } from "./application-stage";
import { PipelineStack } from "./pipeline-stack";

const app = PDKNag.app();

// The stack which defines the CI/CD Pipeline, deploying the below stages.
const pipelineStack = new PipelineStack(app, "PipelineStack", {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT!,
    region: process.env.CDK_DEFAULT_REGION!,
  },
});

// The "Dev" stage is currently the only stage in the pipeline. It's recommended to replace the below account/region
// with hardcoded values based on your desired environments for each stage. We recommend a separate account per-stage
// to minimise blast radius.
const devStage = new ApplicationStage(app, "Dev", {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT!,
    region: process.env.CDK_DEFAULT_REGION!,
  },
});

// Sandbox stage is used for development
new ApplicationStage(app, "Sandbox", {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT!,
    region: process.env.CDK_DEFAULT_REGION!,
  },
});

pipelineStack.pipeline.addStage(devStage);

// Add additional stages here i.e. Prod

app.synth();
