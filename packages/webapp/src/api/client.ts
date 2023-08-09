// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import {
  Middleware,
  DefaultApi,
  Configuration,
} from '@aws/api-typescript-runtime';
import { Auth } from 'aws-amplify';
import { AwsV4Signer } from 'aws4fetch';

// @ts-ignore
const { region, sourceApiUrl } = window.runtimeConfig;

/**
 * This middleware signs requests with the logged in user credentials using AWS Signature Version 4.
 */
const sigv4SignMiddleware: Middleware = {
  pre: async ({ init, url }) => {
    const { accessKeyId, secretAccessKey, sessionToken } =
      await Auth.currentCredentials();
    const {
      url: signedUrl,
      headers,
      body,
      method,
    } = await new AwsV4Signer({
      accessKeyId,
      secretAccessKey,
      sessionToken,
      region,
      service: 'execute-api',
      url,
      body: init.body,
      headers: init.headers,
      method: init.method,
    }).sign();
    return {
      url: signedUrl.toString(),
      init: {
        ...init,
        headers,
        body,
        method,
      },
    };
  },
};

const addHeadersMiddleware: Middleware = {
  pre: async ({ init, url }) => ({
    url,
    init: {
      ...init,
      headers: {
        ...init.headers,
        'Content-Type': 'application/json',
      },
    },
  }),
};

const API = new DefaultApi(
  new Configuration({
    // Remove trailing slash if present
    basePath: sourceApiUrl.endsWith('/')
      ? sourceApiUrl.slice(0, -1)
      : sourceApiUrl,
    fetchApi: window.fetch.bind(window),
    middleware: [addHeadersMiddleware, sigv4SignMiddleware],
  }),
);

export { API };
