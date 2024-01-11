import { UserIdentity } from "@aws/pdk/identity";
import { Stack, StackProps } from "aws-cdk-lib";
import { Construct } from "constructs";
import { ApiConstruct } from "../constructs/api";
import { WebsiteConstruct } from "../constructs/website";

export class ApplicationStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const userIdentity = new UserIdentity(this, `${id}UserIdentity`);
    const apiConstruct = new ApiConstruct(this, "Api", {
      userIdentity,
    });
    new WebsiteConstruct(this, "Website", { userIdentity, apiConstruct });
  }
}
