// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { Api, ApiProps } from "@aws/api";
import { OperationConfig } from "@aws/api-typescript";
import { OpenApiIntegration } from "@aws-prototyping-sdk/open-api-gateway";
import { Construct } from "constructs";
export declare type ApiIntegrations = OperationConfig<OpenApiIntegration>;

/**
 * Type-safe construct for the API Gateway resources defined by the spec.
 * You will likely not need to modify this file, and can instead extend it and define your integrations.
 */
export class ApiExtended extends Api {
  integrations: ApiIntegrations;
  constructor(scope: Construct, id: string, props: ApiProps) {
    super(scope, id, props);
    this.integrations = props.integrations;
  }
}
