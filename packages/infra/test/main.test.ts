// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { App } from "aws-cdk-lib";
import { Template } from "aws-cdk-lib/assertions";
import { ApplicationStack } from "../src/stacks/application-stack";

test("Snapshot", () => {
  const app = new App();
  const stack = new ApplicationStack(app, "test");

  const template = Template.fromStack(stack);
  expect(template.toJSON()).toMatchSnapshot();
});
