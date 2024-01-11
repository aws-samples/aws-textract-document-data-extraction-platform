import { MonorepoTsProject } from "@aws/pdk/monorepo";
import { NodePackageManager } from "projen/lib/javascript";

const monorepo = new MonorepoTsProject({
  devDeps: ["@aws/pdk"],
  name: "@aws/document-extraction-platform",
  packageManager: NodePackageManager.PNPM,
  projenrcTs: true,
});

monorepo.synth();
