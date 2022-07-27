// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { Project } from "projen";
import { PythonProject } from "projen/lib/python";
import { configureProject } from "./utils/common";
import { licenseFile, LicenseVariant } from "./utils/license";

export interface LambdasProjectProps {
  readonly monorepo: Project;
}

const MODULE_NAME = "aws_lambdas";
const ENV_DIR = "../../.env";

/**
 * Synthesize the lambdas project
 */
export const lambdasProject = ({
  monorepo,
}: LambdasProjectProps): PythonProject => {
  const lambdas = new PythonProject({
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
    ],
    devDeps: [
      "mypy",
      "black",
      "licenseheaders",
      "moto",
      "boto3-stubs[s3]",
      "types-python-dateutil",
    ],
    venvOptions: {
      envdir: ENV_DIR,
    },
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

  // Indicate that the python client has inline types by creating a py.typed file
  // postCompileTask.exec(
  //   `touch ${ENV_DIR}/lib/python3.9/site-packages/api_python_client/py.typed`
  // );

  // Run type checking as a post compile step
  postCompileTask.exec(`mypy ${MODULE_NAME}`);

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

  // Create a dist folder for our lambdas with only prod dependencies
  const packageTask = lambdas.tasks.tryFind("package")!;
  packageTask.exec(`mkdir -p dist && rm -rf dist/*`);
  packageTask.exec(`cp -r ${MODULE_NAME} dist/${MODULE_NAME}`);
  packageTask.exec(`pip3 install -r requirements.txt -t dist`);

  return lambdas;
};
