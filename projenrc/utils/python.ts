import * as path from "path";
import { PythonProject } from "projen/lib/python";


export const configurePyProject = (project: PythonProject) => {
  project.addDevDependency("black@^22");
  project.addDevDependency("licenseheaders@0.8.8");

  const licenseHeader = path.join(path.relative(project.outdir, project.parent!.outdir), "header.txt");
  const lintTask = project.addTask("lint");
  lintTask.exec(
    `licenseheaders -E .py -x '*/__init__.py' -d ${project.moduleName} -t ${licenseHeader}`
  );
  lintTask.exec(
    `if [ -d tests ]; then licenseheaders -E .py -x '*/__init__.py' -d tests -t ${licenseHeader}; fi`
  );
  lintTask.exec(
    `if [ -d test ]; then licenseheaders -E .py -x '*/__init__.py' -d test -t ${licenseHeader}; fi`
  );
  lintTask.exec(`black ${project.moduleName}`);
  lintTask.exec("if [ -d tests ]; then black tests; fi");
  lintTask.exec("if [ -d test ]; then black test; fi");
  project.testTask.spawn(lintTask);
};
