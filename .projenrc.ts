import { nx_monorepo } from "aws-prototyping-sdk";
const project = new nx_monorepo.NxMonorepoProject({
  defaultReleaseBranch: "main",
  devDeps: ["aws-prototyping-sdk"],
  name: "document-data-extraction-platform",

  // deps: [],                /* Runtime dependencies of this module. */
  // description: undefined,  /* The description is just a string that helps people understand the purpose of the package. */
  // packageName: undefined,  /* The "name" in package.json. */
});
project.synth();
