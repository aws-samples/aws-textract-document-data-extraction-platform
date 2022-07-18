# Infra

This package contains the CDK infrastructure for the prototype. It defines a CI/CD pipeline which deploys the prototype
to one or more stages. It is recommended to deploy each stage to a separate AWS account.

## Bootstrapping New Accounts

To add an AWS account to the pipeline, first ensure the new account is bootstrapped to trust the pipeline account:

```bash
cdk bootstrap --profile <target account profile> --trust <pipeline account id> --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess
```

Next, update `src/pipeline.ts` to add the new stage, specifying the new account ID and region. The code change can then
be pushed and the pipeline will update automatically.
