// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { Duration, Stack } from "aws-cdk-lib";
import {
  FunctionProps,
  Function as LambdaFunction,
  Runtime,
  Code,
  LayerVersion,
} from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";

export interface PythonLambdaProps
  extends Omit<FunctionProps, "runtime" | "handler" | "code"> {
  handler: string;
}

const SINGLETON_LAMBDA_LAYER_CONSTRUCT_NAME = "ApiPythonLayer";
/**
 * Construct to create a lambda function from code defined in the "lambdas" package
 */
export class PythonLambda extends LambdaFunction {
  /**
   * Create or return the single layer for all python lambdas within the stack
   */
  public static singletonLambdaLayer(scope: Construct): LayerVersion {
    const stack = Stack.of(scope);

    const existingLayer = stack.node.tryFindChild(
      SINGLETON_LAMBDA_LAYER_CONSTRUCT_NAME
    );
    if (existingLayer) {
      return existingLayer as LayerVersion;
    }
    const pythonLayer = new LayerVersion(
      stack,
      SINGLETON_LAMBDA_LAYER_CONSTRUCT_NAME,
      {
        code: Code.fromAsset("../api/generated/python/dist/layer"),
      }
    );

    return pythonLayer;
  }

  constructor(
    scope: Construct,
    id: string,
    { handler, ...props }: PythonLambdaProps
  ) {
    super(scope, id, {
      layers: [PythonLambda.singletonLambdaLayer(scope)],
      runtime: Runtime.PYTHON_3_9,
      code: Code.fromAsset("../lambdas/dist"),
      handler: `aws_lambdas/${handler}.handler`,
      timeout: Duration.seconds(30),
      memorySize: 256,
      ...props,
    });
  }
}
