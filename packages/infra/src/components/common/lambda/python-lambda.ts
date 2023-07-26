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

export interface PythonLambdaProps
  extends Omit<FunctionProps, "runtime" | "handler" | "code"> {
  handler: string;
}

/**
 * Construct to create a lambda function from code defined in the "lambdas" package
 */
export class PythonLambda extends LambdaFunction {
  constructor(
    scope: Construct,
    id: string,
    { handler, ...props }: PythonLambdaProps
  ) {
    super(scope, id, {
      runtime: Runtime.PYTHON_3_9,
      code: Code.fromAsset("../lambdas/lambda-dist"),
      handler: `aws_lambdas/${handler}.handler`,
      timeout: Duration.seconds(30),
      memorySize: 256,
      ...props,
    });
  }
}
