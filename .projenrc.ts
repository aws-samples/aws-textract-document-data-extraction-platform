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

api.handlers.python!.addDependency("boto3@^1");
api.handlers.python!.addDependency("botocore@^1");

const pythonLibrary = new PythonProject({
  parent: monorepo,
  poetry: true,
  sample: false,
  outdir: "packages/lib",
  name: "aws-document-extraction-platform-lib",
  moduleName: "aws_document_extraction_platform_lib",
  authorEmail: "aws@amazon.com",
  authorName: "aws",
  version: "0.0.0",
  deps: [
    "python@^3.9",
    "boto3@^1",
    "botocore@^1",
    "amazon-textract-response-parser@^1",
    "pypdf2@^1",
    "thefuzz@^0.19",
  ],
  devDeps: [
    "black@^22",
    "licenseheaders@^0.8.8",
    "moto@^4",
    `boto3-stubs@{version="^1", extras=["s3"]}`,
    "types-python-dateutil@^2",
  ],
});
monorepo.addPythonPoetryDependency(pythonLibrary, api.runtime.python!);
monorepo.addPythonPoetryDependency(api.handlers.python!, pythonLibrary);

// Create a lambda distributable for the state machine handlers included in the python library
pythonLibrary.packageTask.exec("mkdir -p dist/lambda && rm -rf dist/lambda/*");
pythonLibrary.packageTask.exec(
  `cp -r ${pythonLibrary.moduleName} dist/lambda/${pythonLibrary.moduleName}`
);
pythonLibrary.packageTask.exec(
  "poetry export --without-hashes --format=requirements.txt > dist/lambda/requirements.txt"
);
pythonLibrary.packageTask.exec(
  `pip install -r dist/lambda/requirements.txt --target dist/lambda --upgrade --platform manylinux2014_x86_64 --only-binary :all:`
);

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
