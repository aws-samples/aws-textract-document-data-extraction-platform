// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { nx_monorepo } from "aws-prototyping-sdk";
import { Component } from "projen";
import { exec } from "projen/lib/util";
import { apiProject } from "./projenrc/api";
import { infraProject } from "./projenrc/infra";
import { lambdasProject } from "./projenrc/lambdas";
import { configureProject } from "./projenrc/utils/common";
import { configureTsProject } from "./projenrc/utils/typescript";
import { webappProject } from "./projenrc/webapp";

const awsPrototypingSdkVersion = "0.10.0";
const cdkVersion = "2.23.0";
const constructsVersion = "10.0.77";
const monorepo = new nx_monorepo.NxMonorepoProject({
  defaultReleaseBranch: "main",
  devDeps: ["aws-prototyping-sdk", "eslint-plugin-header"],
  name: "monorepo",
  // License written separately
  licensed: false,
  eslintOptions: {
    dirs: [],
    devdirs: ["projenrc"],
  },
});
configureProject(monorepo);
configureTsProject(monorepo);
monorepo.addDevDeps(
  `aws-prototyping-sdk@${awsPrototypingSdkVersion}`,
  `@aws-prototyping-sdk/open-api-gateway@${awsPrototypingSdkVersion}`
);
monorepo.tryFindObjectFile("package.json")?.addOverride("resolutions", {
  "**/aws-cdk-lib": cdkVersion,
  "**/constructs": constructsVersion,
  "**/@types/react": "^17",
  "**/react": "^17",
  "**/react-dom": "^17",
  "**/@types/react-dom": "^17",
});
monorepo.gitignore.addPatterns(".vscode/*");
monorepo.gitignore.addPatterns(".env/*");
monorepo.gitignore.addPatterns(".DS_Store");
// Lint this file and other projen code as part of post synthesize
monorepo.components.push(
  new (class extends Component {
    postSynthesize(): void {
      exec(
        `eslint --ext .ts --fix --no-error-on-unmatched-pattern projenrc .projenrc.ts`,
        { cwd: monorepo.outdir }
      );
    }
  })(monorepo)
);

const cdkDeps = [
  `aws-cdk-lib@${cdkVersion}`,
  `constructs@${constructsVersion}`,
];

const api = apiProject({ monorepo, cdkDeps });
const lambdas = lambdasProject({ monorepo });

monorepo.addImplicitDependency(lambdas, api);

const webapp = webappProject({ monorepo });
webapp.addDeps(api.generatedTypescriptClient.package.packageName);

monorepo.addImplicitDependency(webapp, api);

const infra = infraProject({
  monorepo,
  constructsVersion,
  cdkVersion,
  cdkDeps,
  awsPrototypingSdkVersion,
});
infra.addDeps(api.package.packageName);
monorepo.addImplicitDependency(infra, lambdas);

monorepo.synth();
