// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { ArnFormat, Stack } from "aws-cdk-lib";
import {
  Effect,
  PolicyStatement,
  Role,
  ServicePrincipal,
} from "aws-cdk-lib/aws-iam";
import { Key } from "aws-cdk-lib/aws-kms";
import { Bucket } from "aws-cdk-lib/aws-s3";
import { Topic } from "aws-cdk-lib/aws-sns";
import { LambdaSubscription } from "aws-cdk-lib/aws-sns-subscriptions";
import {
  IntegrationPattern,
  JsonPath,
  StateMachine,
  TaskInput,
} from "aws-cdk-lib/aws-stepfunctions";
import { LambdaInvoke } from "aws-cdk-lib/aws-stepfunctions-tasks";
import { Construct } from "constructs";
import { PythonLibLambda } from "../../common/lambda/python-lib-lambda";

export interface TextractStateMachineProps {
  readonly sourceBucket: Bucket;
}

/**
 * State machine for running a textract document analysis job.
 * Reused by both classification and extraction workflows.
 */
export class TextractStateMachine extends Construct {
  public readonly stateMachine: StateMachine;

  constructor(
    scope: Construct,
    id: string,
    { sourceBucket }: TextractStateMachineProps,
  ) {
    super(scope, id);

    const buildLambda = (handler: string) =>
      new PythonLibLambda(this, handler, {
        handler: `textract_state_machine/${handler}`,
      });

    // Lambda for starting a textract job
    const startLambda = buildLambda("start_job");
    startLambda.addToRolePolicy(
      new PolicyStatement({
        effect: Effect.ALLOW,
        actions: ["textract:StartDocumentAnalysis"],
        resources: ["*"],
      }),
    );
    sourceBucket.grantRead(startLambda);

    const topicMasterKey = new Key(this, "MyKey", {
      enableKeyRotation: true,
    });

    // SNS topic for textract to report success to
    const topic = new Topic(this, "TextractTopic", {
      masterKey: topicMasterKey,
    });

    // Role for textract to publish messages to the topic
    const publishRole = new Role(this, "PublishRole", {
      assumedBy: new ServicePrincipal("textract.amazonaws.com"),
    });
    topic.grantPublish(publishRole);
    topicMasterKey.grantEncryptDecrypt(publishRole);

    // We create a lambda invoke task with the "wait for task token" service integration pattern, so that this step
    // is only marked as complete once reported with the task token
    const runTextract = new LambdaInvoke(this, "RunTextract", {
      lambdaFunction: startLambda,
      payload: TaskInput.fromObject({
        document_location: TaskInput.fromJsonPathAt(
          "$.Payload.DocumentLocation",
        ).value,
        feature_types: JsonPath.stringAt("$.Payload.FeatureTypes"),
        extra_textract_args: JsonPath.stringAt("$.Payload.ExtraTextractArgs"),
        task_token: JsonPath.taskToken,
        sns_topic_arn: topic.topicArn,
        role_arn: publishRole.roleArn,
        // Execution "Name" is the ID part without the arn prefix, which is used since the full arn is >64
        // characters which is the maximum length for the JobTag, used to track which execution started the textract
        // job when it completes
        execution_id: JsonPath.stringAt("$$.Execution.Name"),
      }),
      integrationPattern: IntegrationPattern.WAIT_FOR_TASK_TOKEN,
    });
    this.stateMachine = new StateMachine(this, "TextractStateMachine", {
      definition: runTextract,
      tracingEnabled: true,
    });

    // Lambda called when a textract job completes, responsible for reporting success/failure
    const onCompleteLambda = buildLambda("on_complete");
    topic.addSubscription(new LambdaSubscription(onCompleteLambda));

    // Grant the on complete lambda permissions to report success/failure of a task
    this.stateMachine.grantTaskResponse(onCompleteLambda);

    // Grant the on complete lambda permissions to read execution history to find the task token to report with
    this.stateMachine.grantRead(onCompleteLambda);

    // Grant the on complete lambda the ability to abort an execution if an unexpected error occurs
    onCompleteLambda.addToRolePolicy(
      new PolicyStatement({
        effect: Effect.ALLOW,
        actions: ["states:StopExecution"],
        resources: [
          Stack.of(this).formatArn({
            service: "states",
            resource: "execution",
            resourceName: `${this.stateMachine.stateMachineName}:*`,
            arnFormat: ArnFormat.COLON_RESOURCE_NAME,
          }),
        ],
      }),
    );

    onCompleteLambda.addEnvironment(
      "STATE_MACHINE_ARN",
      this.stateMachine.stateMachineArn,
    );
  }
}
