# Web App

This contains the code for the front end React website.

## Development

### Runtime Configuration

To develop locally, you'll want to point your local website at a particular backend. The website
expects runtime configuration to be available at `public/runtime-configuration.js`, containing all
configuration required to point to the appropriate API, Cognito pool, etc.

To quickly retrieve the runtime configuration for a particular deployment, you can use the following `curl` command:

```bash
curl https://dxxxxxxxxxx.cloudfront.net/runtime-configuration.js > public/runtime-configuration.js
```

Replace the `dxxxxxxxxxx.cloudfront.net` above with your distribution domain name (output after a successful deployment).

### Start a local dev server

In the root of the monorepo:

```bash
npx nx run @aws/webapp:dev
```
