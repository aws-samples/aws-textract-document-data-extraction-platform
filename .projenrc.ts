import { MonorepoTsProject } from "@aws/pdk/monorepo";
import { DocumentationFormat, Language, Library, ModelLanguage, TypeSafeApiProject } from "@aws/pdk/type-safe-api";
import { CloudscapeReactTsWebsiteProject } from "@aws/pdk/cloudscape-react-ts-website";
import { InfrastructureTsProject } from "@aws/pdk/infrastructure";
import { NodePackageManager } from "projen/lib/javascript";
import { PythonProject } from "projen/lib/python";
import * as path from "path";
import { DependencyType } from "projen";
import { configureTsProject } from "./projenrc/utils/typescript";
import { configureProject } from "./projenrc/utils/common";
import { configurePyProject } from "./projenrc/utils/python";

const monorepo = new MonorepoTsProject({
  devDeps: ["@aws/pdk"],
  name: "@aws/document-extraction-platform",
  packageManager: NodePackageManager.PNPM,
  projenrcTs: true,
});
configureTsProject(monorepo);

monorepo.package.addPackageResolutions("fast-xml-parser@^4.2.5", "nth-check@^2.0.1", "semver@^7.5.2");

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
configurePyProject(api.handlers.python!);

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
    "python@^3.11",
    "boto3@^1",
    "botocore@^1",
    "amazon-textract-response-parser@^1",
    "pypdf2@^1",
    "thefuzz@^0.19",
  ],
  devDeps: [
    "moto@^4",
    `boto3-stubs@{version="^1", extras=["s3"]}`,
    "types-python-dateutil@^2",
  ],
});
configurePyProject(pythonLibrary);
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


const webapp = new CloudscapeReactTsWebsiteProject({
  parent: monorepo,
  outdir: "packages/webapp",
  name: "@aws/document-extraction-platform-webapp",
  typeSafeApi: api,
  deps: [
    "aws-amplify@4.3.8",
    "@aws-amplify/ui-react@1.2.5",
    "aws-northstar",
    "aws4fetch",
    "react-pdf@^5",
    "react-ace@^10",
    "ace-builds@^1",
    "@material-ui/icons@^4",
    "lodash",
    "humanize-duration",
    "react-zoom-pan-pinch@^2",
    "react-router-dom@^5",
  ],
  devDeps: [
    "@types/lodash",
    "@types/humanize-duration",
    "react-app-rewired@^2",
    "@types/react-router-dom",
    "@types/react-pdf@^5",
  ],
});
configureTsProject(webapp);

// TODO: Consider upgrading to northstar v2 / cloudscape
webapp.deps.removeDependency("@aws-northstar/ui");
webapp.deps.removeDependency("@cloudscape-design/components");
webapp.deps.removeDependency("@cloudscape-design/board-components");

monorepo.package.addPackageResolutions("react-router-dom@^5");

// TODO: Consider upgrade to react 18
[webapp, api.library.typescriptReactQueryHooks!].forEach(project => {
  project.deps.removeDependency("react", DependencyType.BUILD);
  project.deps.removeDependency("react", DependencyType.PEER);
  project.deps.removeDependency("@types/react");
  project.deps.removeDependency("react-dom");
  project.deps.removeDependency("@types/react-dom");
  project.addDeps("react@^17");
  project.addDeps("react-dom@^17");
  project.addDevDeps("@types/react@^17");
  project.addDevDeps("@types/react-dom@^17");
});

// Use react-app-rewired tasks instead of default create react app tasks.
  // Note that we disable the inbuilt create react app eslint plugin in favour of running our own eslint after the tests
  webapp.tasks.tryFind("dev")?.reset();
  webapp.tasks
    .tryFind("dev")
    ?.exec("DISABLE_ESLINT_PLUGIN=true react-app-rewired start");
  webapp.tasks.tryFind("compile")?.reset();
  webapp.tasks
    .tryFind("compile")
    ?.exec("DISABLE_ESLINT_PLUGIN=true react-app-rewired build --verbose");
  webapp.tasks.tryFind("test")?.reset();
  webapp.tasks
    .tryFind("test")
    ?.exec(
      "DISABLE_ESLINT_PLUGIN=true react-app-rewired test --watchAll=false"
    );
  webapp.tasks.tryFind("test")?.spawn(webapp.tasks.tryFind("eslint")!);
  webapp.tasks.tryFind("test:watch")?.reset();
  webapp.tasks
    .tryFind("test:watch")
    ?.exec("DISABLE_ESLINT_PLUGIN=true react-app-rewired test");

const copyApiDocs = webapp.addTask("copy:api-docs");
copyApiDocs.exec("rm -rf public/api-docs");
copyApiDocs.exec("mkdir -p public/api-docs");
copyApiDocs.exec(`cp -r ${path.relative(webapp.outdir, api.documentation.htmlRedoc!.outdir)}/index.html public/api-docs/index.html`);
webapp.preCompileTask.spawn(copyApiDocs);
monorepo.addImplicitDependency(webapp, api.documentation.htmlRedoc!);


const infra = new InfrastructureTsProject({
  parent: monorepo,
  outdir: "packages/infra",
  name: "@aws/document-extraction-platform-infra",
  deps: [
    api.infrastructure.typescript!.package.packageName,
    api.runtime.typescript!.package.packageName,
    "cdk-nag",
  ],
});
configureTsProject(infra);

monorepo.addImplicitDependency(infra, api.handlers.python!);
monorepo.addImplicitDependency(infra, webapp);

monorepo.addTask("bootstrap", { receiveArgs: true }).exec(`nx run ${infra.name}:bootstrap`, { receiveArgs: true });
monorepo.addTask("deploy", { receiveArgs: true }).exec(`nx run ${infra.name}:deploy --require-approval never --all`, { receiveArgs: true });
monorepo.addTask("destroy", { receiveArgs: true }).exec(`nx run ${infra.name}:destroy --require-approval never --all`, { receiveArgs: true });
monorepo.addTask("dev", { receiveArgs: true }).exec(`nx run ${webapp.name}:dev`, { receiveArgs: true });

monorepo.subprojects.forEach(p => configureProject(p));
configureProject(monorepo);

monorepo.synth();
