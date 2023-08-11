// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { CfnOutput, RemovalPolicy, Stack, StackProps } from "aws-cdk-lib";
import {
  CfnDistribution,
  Distribution,
  SecurityPolicyProtocol,
  ViewerProtocolPolicy,
} from "aws-cdk-lib/aws-cloudfront";
import { S3Origin } from "aws-cdk-lib/aws-cloudfront-origins";
import {
  BlockPublicAccess,
  Bucket,
  BucketEncryption,
  CfnBucket,
  ObjectOwnership,
} from "aws-cdk-lib/aws-s3";
import {
  BucketDeployment,
  ServerSideEncryption,
  Source,
} from "aws-cdk-lib/aws-s3-deployment";
import { Construct } from "constructs";
import { addCfnNagSuppressions } from "../../cfn-nag";

export interface WebsiteStackProps extends StackProps {}

/**
 * Creates infrastructure components for a S3/Cloudfront React website
 */
export class WebsiteStack extends Stack {
  public readonly websiteBucket: Bucket;
  public readonly bucketDeployment: BucketDeployment;
  public readonly distribution: Distribution;

  constructor(scope: Construct, id: string, props: WebsiteStackProps) {
    super(scope, id, props);

    this.websiteBucket = new Bucket(this, "WebsiteBucket", {
      publicReadAccess: false,
      blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
      enforceSSL: true,
      removalPolicy: RemovalPolicy.DESTROY,
    });

    this.distribution = new Distribution(this, "WebsiteDistribution", {
      defaultBehavior: {
        origin: new S3Origin(this.websiteBucket),
        viewerProtocolPolicy: ViewerProtocolPolicy.HTTPS_ONLY,
      },
      enableLogging: true,
      defaultRootObject: "index.html",
      minimumProtocolVersion: SecurityPolicyProtocol.TLS_V1_2_2018,
      logBucket: new Bucket(this, "WebsiteDistributionLoggingBucket", {
        enforceSSL: true,
        publicReadAccess: false,
        blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
        removalPolicy: RemovalPolicy.DESTROY,
        encryption: BucketEncryption.S3_MANAGED,
        objectOwnership: ObjectOwnership.OBJECT_WRITER,
      }),
    });

    this.bucketDeployment = new BucketDeployment(this, "WebsiteDeployment", {
      destinationBucket: this.websiteBucket,
      distribution: this.distribution,
      serverSideEncryption: ServerSideEncryption.AES_256,
      sources: [Source.asset("../webapp/build")],
    });

    // cdk nag suppressions for public bucket
    const cfnWebBucket = this.websiteBucket.node.defaultChild as CfnBucket;
    addCfnNagSuppressions(cfnWebBucket, [
      {
        id: "AwsSolutions-S2",
        reason:
          "This is the bucket that has the website hosted. It has to be public.",
      },
      {
        id: "AwsSolutions-S3",
        reason:
          "This is the bucket that has the website hosted. It has to be public. Data does not need to be encrypted at rest.",
      },
    ]);

    const cfnDistribution = this.distribution.node
      .defaultChild as CfnDistribution;
    addCfnNagSuppressions(cfnDistribution, [
      {
        id: "AwsSolutions-CFR4",
        reason:
          "Raised due to no custom cert provided in the cloudfront distribution.",
      },
    ]);

    new CfnOutput(this, "DistributionDomainName", {
      exportName: "DistributionDomainName",
      value: this.distribution.distributionDomainName,
    });
  }
}
