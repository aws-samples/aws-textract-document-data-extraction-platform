// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { CfnOutput, RemovalPolicy, Stack, StackProps } from "aws-cdk-lib";
import { Distribution } from "aws-cdk-lib/aws-cloudfront";
import { S3Origin } from "aws-cdk-lib/aws-cloudfront-origins";
import { BlockPublicAccess, Bucket } from "aws-cdk-lib/aws-s3";
import {
  BucketDeployment,
  ServerSideEncryption,
  Source,
} from "aws-cdk-lib/aws-s3-deployment";
import { Construct } from "constructs";

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
      },
      defaultRootObject: "index.html",
    });

    this.bucketDeployment = new BucketDeployment(this, "WebsiteDeployment", {
      destinationBucket: this.websiteBucket,
      distribution: this.distribution,
      serverSideEncryption: ServerSideEncryption.AES_256,
      sources: [Source.asset("../webapp/build")],
    });

    new CfnOutput(this, "DistributionDomainName", {
      exportName: "DistributionDomainName",
      value: this.distribution.distributionDomainName,
    });
  }
}
