import { MonorepoTsProject } from "@aws/pdk/monorepo";
import { DocumentationFormat, Language, Library, ModelLanguage, TypeSafeApiProject } from "@aws/pdk/type-safe-api";
import { CloudscapeReactTsWebsiteProject } from "@aws/pdk/cloudscape-react-ts-website";
import { InfrastructureTsProject } from "@aws/pdk/infrastructure";
import { NodePackageManager } from "projen/lib/javascript";
import { PythonProject } from "projen/lib/python";

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

const pythonLibrary = new PythonProject({
  parent: monorepo,
  poetry: true,
  outdir: "packages/lib",
  name: "aws-document-extraction-platform-lib",
  moduleName: "aws_document_extraction_platform_lib",
  authorEmail: "aws@amazon.com",
  authorName: "aws",
  version: "0.0.0",
  deps: [
    "python@^3.9",
  ],
});

monorepo.addPythonPoetryDependency(pythonLibrary, api.runtime.python!);
monorepo.addPythonPoetryDependency(api.handlers.python!, pythonLibrary);

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
