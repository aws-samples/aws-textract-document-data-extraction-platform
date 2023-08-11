// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { DocumentationFormat } from "@aws-prototyping-sdk/open-api-gateway";
import {
  TypeSafeApiProject,
  ModelLanguage,
  Language,
} from "@aws-prototyping-sdk/type-safe-api";
import { Project } from "projen";
import { configureProject } from "./utils/common";

export interface ApiProjectProps {
  readonly monorepo: Project;
}

/**
 * Synthesize the api project
 */
export const apiProject = ({
  monorepo,
}: ApiProjectProps): TypeSafeApiProject => {
  const api = new TypeSafeApiProject({
    name: "@aws/api",
    parent: monorepo,
    outdir: "packages/api",
    model: {
      language: ModelLanguage.OPENAPI,
      options: {
        openapi: { title: "AWS Docs API" },
      },
    },
    runtime: {
      languages: [Language.TYPESCRIPT, Language.PYTHON],
    },
    infrastructure: {
      language: Language.TYPESCRIPT,
      options: {
        typescript: {
          mockDataOptions: {
            disable: true,
          },
          tsconfig: {
            compilerOptions: {
              skipLibCheck: true,
              lib: ["es2019", "dom"],
            },
            exclude: ["node_modules"],
          },
        } as any,
      },
    },
    documentation: {
      formats: [DocumentationFormat.HTML2],
    },
    // typescriptClientOptions: {
    //   defaultReleaseBranch: "mainline",
    //   name: "@aws/api-typescript",
    //   tsconfig: {
    //     compilerOptions: {
    //       skipLibCheck: true,
    //       lib: ["es2019", "dom"],
    //     },
    //   },
    // },
    // pythonClientOptions: {
    //   name: "api_python_client",
    //   moduleName: "api_python_client",
    //   version: "0.0.0",
    //   authorName: "aws",
    //   authorEmail: "aws@aws.com",
    //   venvOptions: {
    //     envdir: "../../../../.env",
    //   },
    // },
  });

  // CDK dependencies are added here since the deps/devDeps arrays above do not always honour specific types
  // api.package.addDevDeps(...cdkDeps);
  // api.package.addPeerDeps(...cdkDeps);

  // TODO: revisit license
  // Add general configuration
  configureProject(api);
  // configureTsProject(api);

  // (api.generatedClients[ClientLanguage.PYTHON] as PythonProject).tasks
  //   .tryFind("install")!
  //   .exec(`pip3 install . --target dist/layer/python`);

  return api;
};
