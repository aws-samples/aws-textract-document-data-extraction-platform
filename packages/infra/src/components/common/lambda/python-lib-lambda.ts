// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { Duration } from "aws-cdk-lib";
import {
  FunctionProps,
  Function as LambdaFunction,
  Runtime,
  Code,
} from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";

export interface PythonLibLambdaProps
  extends Omit<FunctionProps, "runtime" | "handler" | "code"> {
  handler: string;
}

/**
 * Construct to create a lambda function from code defined in the python "lib" package
 */
export class PythonLibLambda extends LambdaFunction {
  constructor(
    scope: Construct,
    id: string,
    { handler, ...props }: PythonLibLambdaProps,
  ) {
    super(scope, id, {
      runtime: Runtime.PYTHON_3_11,
      code: Code.fromAsset("../lib/dist/lambda"),
      handler: `aws_document_extraction_platform_lib/${handler}.handler`,
      timeout: Duration.seconds(30),
      memorySize: 256,
      ...props,
    });
  }
}
