// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { Project } from "projen";
import { ReactTypeScriptProject } from "projen/lib/web";
import { configureProject } from "./utils/common";
import { configureTsProject } from "./utils/typescript";

export interface WebappProjectProps {
  readonly monorepo: Project;
}

/**
 * Synthesize the webapp project
 */
export const webappProject = ({
  monorepo,
}: WebappProjectProps): ReactTypeScriptProject => {
  const webapp = new ReactTypeScriptProject({
    defaultReleaseBranch: "mainline",
    name: "@aws/webapp",
    parent: monorepo,
    outdir: "packages/webapp",
    // License managed separately below
    licensed: false,
    deps: [
      "aws-amplify@4.3.8",
      "graphql",
      "@aws-amplify/ui-react@1.2.5",
      "@aws-amplify/api@1.3.3",
      "@aws-amplify/auth@1.3.3",
      "aws-northstar",
      "aws4fetch",
      "react-pdf",
      "react-ace",
      "ace-builds",
      "@material-ui/icons",
      "lodash",
      "@types/lodash",
      "humanize-duration",
      "react-zoom-pan-pinch",
    ],
    devDeps: ["react-app-rewired", "@types/humanize-duration"],
    eslint: true,
    eslintOptions: {
      dirs: ["src"],
      fileExtensions: [".ts", ".tsx"],
    },
  });
  configureProject(webapp);
  configureTsProject(webapp);

  webapp.package.addDeps("react-router-dom@^5");
  webapp.package.addDevDeps("@testing-library/react@^12");
  webapp.package.addDevDeps("@types/react@^17");
  webapp.package.addDevDeps("@types/react-router-dom@^5");
  webapp.package.addDevDeps("@types/react-pdf");

  // Use react-app-rewired tasks instead of default create react app tasks.
  // Note that we disable the inbuilt create react app eslint plugin in favour of running our own eslint after the tests
  webapp.tasks.tryFind("dev")?.reset();
  webapp.tasks
    .tryFind("dev")
    ?.exec("DISABLE_ESLINT_PLUGIN=true react-app-rewired start");
  webapp.tasks.tryFind("compile")?.reset();
  webapp.tasks
    .tryFind("compile")
    ?.exec("DISABLE_ESLINT_PLUGIN=true react-app-rewired build --verbose");
  webapp.tasks.tryFind("test")?.reset();
  webapp.tasks
    .tryFind("test")
    ?.exec(
      "DISABLE_ESLINT_PLUGIN=true react-app-rewired test --watchAll=false"
    );
  webapp.tasks.tryFind("test")?.spawn(webapp.tasks.tryFind("eslint")!);
  webapp.tasks.tryFind("test:watch")?.reset();
  webapp.tasks
    .tryFind("test:watch")
    ?.exec("DISABLE_ESLINT_PLUGIN=true react-app-rewired test");

  // Copy auto generated openapi docs
  const copyApiDocs = webapp.addTask("copy:api-docs");
  copyApiDocs.exec("rm -rf public/api-docs");
  copyApiDocs.exec("mkdir -p public/api-docs");
  copyApiDocs.exec(
    "cp -r ../api/generated/documentation/html2/* public/api-docs"
  );
  webapp.tasks.tryFind("pre-compile")?.spawn(copyApiDocs);

  webapp.package.addField("config-overrides-path", "./config-overrides.js");
  webapp.gitignore.addPatterns(
    "public/runtime-configuration.js",
    "public/api-docs"
  );

  webapp.eslint?.addRules({
    "import/no-extraneous-dependencies": [
      "error",
      {
        devDependencies: ["**/__tests__/**", "**/setupTests.ts"],
        optionalDependencies: true,
        peerDependencies: true,
      },
    ],
  });

  return webapp;
};
