// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { TypeScriptProject } from "projen/lib/typescript";
import { configureEslint } from "./eslint";

export const configureTsProject = (project: TypeScriptProject) => {
  configureEslint(project);
};
