// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { RemovalPolicy } from "aws-cdk-lib";
import {
  BillingMode,
  Table as DynamoTable,
  TableProps as DynamoTableProps,
} from "aws-cdk-lib/aws-dynamodb";
import { Construct } from "constructs";

export interface TableProps extends DynamoTableProps {
  readonly environmentVariableName: string;
}

/**
 * A dynamodb table with project-wide defaults and extensions
 */
export class Table extends DynamoTable {
  private readonly environmentVariableName: string;

  constructor(
    scope: Construct,
    id: string,
    { environmentVariableName, ...props }: TableProps,
  ) {
    super(scope, id, {
      billingMode: BillingMode.PAY_PER_REQUEST,
      removalPolicy: RemovalPolicy.RETAIN,
      ...props,
    });
    this.environmentVariableName = environmentVariableName;
  }

  /**
   * Return the environment variables to add to any lambdas that make use of the table
   */
  public get environment(): { [key: string]: string } {
    return {
      [this.environmentVariableName]: this.tableName,
    };
  }
}
