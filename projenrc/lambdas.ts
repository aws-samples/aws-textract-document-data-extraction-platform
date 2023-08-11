// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { NxMonorepoProject } from "@aws-prototyping-sdk/nx-monorepo";
import { TypeSafeApiProject } from "@aws-prototyping-sdk/type-safe-api";
import { PythonProject } from "projen/lib/python";
import { configureProject } from "./utils/common";
import { licenseFile, LicenseVariant } from "./utils/license";

export interface LambdasProjectProps {
  readonly monorepo: NxMonorepoProject;
  readonly api: TypeSafeApiProject;
}

const MODULE_NAME = "aws_lambdas";

/**
 * Synthesize the lambdas project
 */
export const lambdasProject = ({
  monorepo,
  api,
}: LambdasProjectProps): PythonProject => {
  const lambdas = new PythonProject({
    poetry: true,
    pip: false,
    authorEmail: "aws@amazon.com",
    authorName: "aws",
    moduleName: MODULE_NAME,
    name: "aws-lambdas",
    version: "1.0.0",
    parent: monorepo,
    outdir: "packages/lambdas",
    deps: [
      "boto3",
      "botocore",
      "amazon-textract-response-parser",
      "pypdf2",
      "thefuzz",
      "python@~3.9",
    ],
    devDeps: [
      "mypy",
      "black",
      "licenseheaders",
      "moto",
      "boto3-stubs[s3]",
      "types-python-dateutil",
      "pytest",
    ],
  });
  configureProject(lambdas);

  const licenseHeader = "header.txt";
  licenseFile({
    project: lambdas,
    fileName: licenseHeader,
    variant: LicenseVariant.SHORT,
  });
  // Add post compile tasks
  const postCompileTask = lambdas.tasks.tryFind("post-compile")!;

  // Run type checking as a post compile step
  postCompileTask.exec(`mypy ${MODULE_NAME}`);
  lambdas.tasks
    .tryFind("install")!
    .prependExec("poetry env info -p || poetry env use python");
  // Add test task
  const testTask = lambdas.tasks.tryFind("test")!;
  testTask.reset();
  // use poetry to run pytest
  testTask.prependExec(`which python`);
  testTask.exec("pytest");
  testTask.exec(`poetry run pytest`);

  // Add linting task to run after tests
  const lintTask = lambdas.addTask("lint");
  lintTask.exec(
    `licenseheaders -E .py -x '*/__init__.py' -d ${MODULE_NAME} -t ${licenseHeader}`
  );
  lintTask.exec(
    `licenseheaders -E .py -x '*/__init__.py' -d tests -t ${licenseHeader}`
  );
  lintTask.exec(`black ${MODULE_NAME}`);
  lintTask.exec("black tests");
  lambdas.tasks.tryFind("test")!.spawn(lintTask);

  // each project will have its own env to install deps
  monorepo.addPythonPoetryDependency(lambdas, api.runtime.python!);

  // Add commands to the lambda project's package task to create a distributable which can be deployed to AWS Lambda
  lambdas.packageTask.exec(`mkdir -p lambda-dist && rm -rf lambda-dist/*`);
  lambdas.packageTask.exec(
    `cp -r ${lambdas.moduleName} lambda-dist/${lambdas.moduleName}`
  );
  lambdas.packageTask.exec(
    `poetry export --without-hashes --format=requirements.txt > lambda-dist/requirements.txt`
  );
  lambdas.packageTask.exec(
    `pip install -r lambda-dist/requirements.txt --target lambda-dist --upgrade`
  );

  return lambdas;
};
