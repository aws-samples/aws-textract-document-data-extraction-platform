// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { PDKPipelineTsProject } from "@aws-prototyping-sdk/pipeline";
import { Project } from "projen";
import { ApprovalLevel } from "projen/lib/awscdk";
import { TypeScriptProject } from "projen/lib/typescript";
import { configureProject } from "./utils/common";
import { configureTsProject } from "./utils/typescript";

export interface InfraProjectProps {
  readonly monorepo: Project;
}

/**
 * Synthesize the cdk infrastructure project
 */
export const infraProject = ({
  monorepo,
}: InfraProjectProps): TypeScriptProject => {
  const infra = new PDKPipelineTsProject({
    defaultReleaseBranch: "mainline",
    name: "@aws/infra",
    cdkVersion: "2.0.0",
    cdkVersionPinning: true,
    appEntrypoint: "pipeline.ts",
    parent: monorepo,
    requireApproval: ApprovalLevel.NEVER,
    outdir: "packages/infra",
    // License written separately
    licensed: false,
    deps: [
      "openapi-types",
      "aws-sdk",
      "uuid",
      `@aws-prototyping-sdk/type-safe-api`,
    ],
    devDeps: ["@types/uuid", "ts-node@10.6.0", "typescript@4.6.4"],
    tsconfig: {
      compilerOptions: {
        skipLibCheck: true,
        lib: ["es2019", "dom"],
      },
    },
    tsconfigDev: {
      compilerOptions: {
        skipLibCheck: true,
        lib: ["es2019", "dom"],
      },
    },
  });

  // Add dependencies that require explicit versions
  infra.package.addDeps(
    ...[`aws-cdk-lib`, `constructs`],
    "@aws-prototyping-sdk/pipeline"
  );

  // Configure linting etc
  configureProject(infra);
  configureTsProject(infra);

  // Add a script for deploying the 'sandbox' stage for developer convenience
  infra.setScript(
    "deploy-sandbox",
    `cdk deploy -a cdk.out/assembly-Sandbox --all`
  );

  return infra;
};
