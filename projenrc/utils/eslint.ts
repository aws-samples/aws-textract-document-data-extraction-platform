// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { TypeScriptProject } from "projen/lib/typescript";
import { getShortLicense } from "./license";

/**
 * Add the MIT-0 header to ts files
 */
const addEslintHeaderConfig = (project: TypeScriptProject) => {
  project.eslint?.addPlugins("header");
  project.eslint?.addRules({
    "header/header": [2, "line", [...getShortLicense()]],
    "import/no-extraneous-dependencies": ["off"],
  });
};

const addEslintRulesConfig = (project: TypeScriptProject) => {
  project.eslint?.addRules({
    "import/no-extraneous-dependencies": ["off"],
  });
};

/**
 * Apply custom eslint config to the project
 */
export const configureEslint = (project: TypeScriptProject) => {
  project.addDevDeps("eslint-plugin-header@^3");
  addEslintHeaderConfig(project);
  addEslintRulesConfig(project);
};
