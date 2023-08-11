// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import path from "path";
import { NxMonorepoProject } from "@aws-prototyping-sdk/nx-monorepo";
import { Component } from "projen";
import { exec } from "projen/lib/util";
import { apiProject } from "./projenrc/api";
import { infraProject } from "./projenrc/infra";
import { lambdasProject } from "./projenrc/lambdas";
import { configureProject } from "./projenrc/utils/common";
import { configureTsProject } from "./projenrc/utils/typescript";
import { webappProject } from "./projenrc/webapp";

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
  "**/@types/react": "^17",
  "**/react": "^17",
  "**/react-dom": "^17",
  "**/@types/react-dom": "^17",
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
});
infra.addDeps(api.infrastructure.typescript!.package.packageName);
infra.addDeps(webapp.package.packageName);
monorepo.addImplicitDependency(infra, lambdas);

monorepo.setScript(
  "preinstall",
  `cd ... ${path.relative(
    monorepo.outdir,
    lambdas.outdir
  )} && poetry env info -p || poetry env use python; cd ${path.relative(
    monorepo.outdir,
    api.runtime.python!.outdir
  )} && poetry env info -p || poetry env use python`
);
monorepo.synth();
