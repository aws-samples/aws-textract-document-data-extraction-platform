// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { NxMonorepoProject } from "@aws-prototyping-sdk/nx-monorepo";
import { Component } from "projen";
import { exec } from "projen/lib/util";
import { apiProject } from "./projenrc/api";
import { infraProject } from "./projenrc/infra";
import { lambdasProject } from "./projenrc/lambdas";
import { configureProject } from "./projenrc/utils/common";
import { configureTsProject } from "./projenrc/utils/typescript";
import { webappProject } from "./projenrc/webapp";

const awsPrototypingSdkVersion = "0.19.47";
const cdkVersion = "2.45.0";
const constructsVersion = "10.1.124";
const monorepo = new NxMonorepoProject({
  defaultReleaseBranch: "main",
  devDeps: ["eslint-plugin-header"],
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
  `@aws-prototyping-sdk/nx-monorepo`,
  "@aws-prototyping-sdk/pipeline",
  `@aws-prototyping-sdk/open-api-gateway`,
  `@aws-prototyping-sdk/type-safe-api`
);
monorepo.tryFindObjectFile("package.json")?.addOverride("resolutions", {
  // "**/aws-cdk-lib": cdkVersion,
  // "**/constructs": constructsVersion,
  // "**/@types/react": "^17",
  // "**/react": "^17",
  // "**/react-dom": "^17",
  // "**/@types/react-dom": "^17",
  // "**/d3-color": "^3.1.0",
  // "**/axios": "^0.21.2",
  // "**/aws-sdk": "^2.814.0",
  // "**/nth-check": "^2.0.1",
  // "**/minimatch": "^3.1.0",
  // "**/loader-utils": "2.0.4",
  // "**/json5": "^2.2.2",
  // "**/decode-uri-component": "^0.2.1",
  // "**/http-cache-semantics": "^4.1.1",
});
monorepo.gitignore.addPatterns(".vscode/*");
monorepo.gitignore.addPatterns(".env/*");
monorepo.gitignore.addPatterns(".DS_Store");
monorepo.gitignore.addPatterns(".nx/*");
monorepo.gitignore.addPatterns("nx.json");
monorepo.gitignore.addPatterns("syncpackrc.json");

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

const api = apiProject({ monorepo });
const lambdas = lambdasProject({ monorepo, api });

monorepo.addImplicitDependency(lambdas, api);

const webapp = webappProject({ monorepo });
configureTsProject(webapp);
// make sure typescript client is generated first
webapp.addDeps(api.runtime.typescript?.package.packageName!);
// documentation gets generated before it is copied
monorepo.addImplicitDependency(webapp, api.documentation.html2!);

const infra = infraProject({
  monorepo,
  constructsVersion,
  cdkVersion,
  cdkDeps,
  awsPrototypingSdkVersion,
});
infra.addDeps(api.infrastructure.typescript!.package.packageName);
infra.addDeps(webapp.package.packageName);
monorepo.addImplicitDependency(infra, lambdas);

// monorepo.tasks.tryFind("default")?.reset();
// monorepo.tasks
//   .tryFind("default")
//   ?.exec("npx ts-node --project tsconfig.dev.json .projenrc.ts");

monorepo.synth();
