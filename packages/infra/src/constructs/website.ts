import { UserIdentity } from "@aws/pdk/identity";
import { StaticWebsite } from "@aws/pdk/static-website";
import { Stack } from "aws-cdk-lib";
import { GeoRestriction } from "aws-cdk-lib/aws-cloudfront";
import { Construct } from "constructs";
import { ApiConstruct } from "./api";

/**
 * Website construct props
 */
export interface WebsiteConstructProps {
  /**
   * Instance of an API to configure the website to integrate with
   */
  readonly apiConstruct: ApiConstruct;

  /**
   * Instance of the UserIdentity.
   */
  readonly userIdentity: UserIdentity;
}

/**
 * Construct to deploy a Static Website
 */
export class WebsiteConstruct extends Construct {
  constructor(scope: Construct, id: string, props?: WebsiteConstructProps) {
    super(scope, id);

    new StaticWebsite(this, id, {
      websiteContentPath: "../website/build",
      runtimeOptions: {
        jsonPayload: {
          region: Stack.of(this).region,
          identityPoolId: props?.userIdentity.identityPool.identityPoolId,
          userPoolId: props?.userIdentity.userPool?.userPoolId,
          userPoolWebClientId:
            props?.userIdentity.userPoolClient?.userPoolClientId,
          apiUrl: props?.apiConstruct.api.api.urlForPath(),
        },
      },
      distributionProps: {
        geoRestriction: GeoRestriction.allowlist(
          "AU",
          "ID",
          "IN",
          "JP",
          "KR",
          "SG",
          "US",
        ),
      },
    });
  }
}
