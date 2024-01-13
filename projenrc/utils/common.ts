// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { Project } from "projen";
import { licenseFile } from "./license";

export const configureProject = (project: Project) => {
  licenseFile({ project });
  project.tryFindObjectFile("package.json")?.addOverride("license", "MIT-0");
};
