/**********************************************************************************************************************
 *  Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                           *
 *                                                                                                                    *
 *  Licensed under the Amazon Software License (the "License"). You may not use this file except in compliance        *
 *  with the License. A copy of the License is located at                                                             *
 *                                                                                                                    *
 *     http://aws.amazon.com/asl/                                                                                     *
 *                                                                                                                    *
 *  or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES *
 *  OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions    *
 *  and limitations under the License.                                                                                *
 **********************************************************************************************************************/
import { Configuration, DefaultApi, Middleware } from '@aws/api-typescript';
import { Auth } from 'aws-amplify';
import { AwsV4Signer } from 'aws4fetch';

// @ts-ignore
const { region, sourceApiUrl } = window.runtimeConfig;

/**
 * This middleware signs requests with the logged in user credentials using AWS Signature Version 4.
 */
const sigv4SignMiddleware: Middleware = {
  pre: async ({ init, url }) => {
    const { accessKeyId, secretAccessKey, sessionToken } = await Auth.currentCredentials();
    const { url: signedUrl, headers, body, method } = await new AwsV4Signer({
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

const API = new DefaultApi(new Configuration({
  // Remove trailing slash if present
  basePath: sourceApiUrl.endsWith('/') ? sourceApiUrl.slice(0, -1) : sourceApiUrl,
  fetchApi: window.fetch.bind(window),
  middleware: [
    addHeadersMiddleware,
    sigv4SignMiddleware,
  ],
}));

export { API };
