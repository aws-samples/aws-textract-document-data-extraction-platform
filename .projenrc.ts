import { MonorepoTsProject } from "@aws/pdk/monorepo";
import { DocumentationFormat, Language, Library, ModelLanguage, TypeSafeApiProject } from "@aws/pdk/type-safe-api";
import { CloudscapeReactTsWebsiteProject } from "@aws/pdk/cloudscape-react-ts-website";
import { InfrastructureTsProject } from "@aws/pdk/infrastructure";
import { NodePackageManager } from "projen/lib/javascript";

const monorepo = new MonorepoTsProject({
  devDeps: ["@aws/pdk"],
  name: "@aws/document-extraction-platform",
  packageManager: NodePackageManager.PNPM,
  projenrcTs: true,
});

const api = new TypeSafeApiProject({
  parent: monorepo,
  outdir: "packages/api",
  name: "@aws/document-extraction-platform-api",
  infrastructure: {
    language: Language.TYPESCRIPT,
  },
  model: {
    language: ModelLanguage.OPENAPI,
    options: {
      openapi: {
        title: "AWS Docs API",
      },
    },
  },
  documentation: {
    formats: [DocumentationFormat.HTML_REDOC],
  },
  handlers: {
    languages: [Language.PYTHON],
  },
  library: {
    libraries: [Library.TYPESCRIPT_REACT_QUERY_HOOKS],
  },
});

const website = new CloudscapeReactTsWebsiteProject({
  parent: monorepo,
  outdir: "packages/website",
  name: "@aws/document-extraction-platform-website",
  typeSafeApi: api,
});

new InfrastructureTsProject({
  parent: monorepo,
  outdir: "packages/infra",
  name: "@aws/document-extraction-platform-infra",
  cloudscapeReactTsWebsite: website,
  typeSafeApi: api,
});

monorepo.synth();
