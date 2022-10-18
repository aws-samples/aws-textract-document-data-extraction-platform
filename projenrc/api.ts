// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import {
  ClientLanguage,
  OpenApiGatewayTsProject,
  DocumentationFormat,
} from "@aws-prototyping-sdk/open-api-gateway";

import { Project } from "projen";
import { PythonProject } from "projen/lib/python";
import { configureProject } from "./utils/common";
import { configureTsProject } from "./utils/typescript";

export interface ApiProjectProps {
  readonly monorepo: Project;
  readonly cdkDeps: string[];
}

/**
 * Synthesize the api project
 */
export const apiProject = ({
  monorepo,
  cdkDeps,
}: ApiProjectProps): OpenApiGatewayTsProject => {
  const api = new OpenApiGatewayTsProject({
    name: "@aws/api",
    clientLanguages: [ClientLanguage.TYPESCRIPT, ClientLanguage.PYTHON],
    defaultReleaseBranch: "mainline",
    documentationFormats: [DocumentationFormat.HTML2],
    sampleCode: false,
    parent: monorepo,
    outdir: "packages/api",
    // License written separately
    licensed: false,
    tsconfig: {
      compilerOptions: {
        skipLibCheck: true,
        lib: ["es2019", "dom"],
      },
    },
    typescriptClientOptions: {
      defaultReleaseBranch: "mainline",
      name: "@aws/api-typescript",
      tsconfig: {
        compilerOptions: {
          skipLibCheck: true,
          lib: ["es2019", "dom"],
        },
      },
    },
    pythonClientOptions: {
      name: "api_python_client",
      moduleName: "api_python_client",
      version: "0.0.0",
      authorName: "aws",
      authorEmail: "aws@aws.com",
      venvOptions: {
        envdir: "../../../../.env",
      },
    },
  });

  // CDK dependencies are added here since the deps/devDeps arrays above do not always honour specific types
  api.package.addDevDeps(...cdkDeps);
  api.package.addPeerDeps(...cdkDeps);

  // Add general configuration
  configureProject(api);
  configureTsProject(api);

  (api.generatedClients[ClientLanguage.PYTHON] as PythonProject).tasks
    .tryFind("install")!
    .exec(`pip3 install . --target dist/layer/python`);

  return api;
};
