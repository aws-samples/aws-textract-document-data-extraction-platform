// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import {
  DefaultApi,
  Configuration,
  Middleware,
} from "@aws/document-extraction-platform-api-typescript-react-query-hooks";
import { Auth } from "aws-amplify";
import { AwsV4Signer } from "aws4fetch";
import { useContext, useMemo } from "react";
import {
  RuntimeConfigContext,
  RuntimeContext,
} from "../components/runtime-context";

const buildClient = (runtimeContext: RuntimeContext): DefaultApi => {
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
        region: runtimeContext.region,
        service: "execute-api",
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

  return new DefaultApi(
    new Configuration({
      basePath: runtimeContext.sourceApiUrl.endsWith("/")
        ? runtimeContext.sourceApiUrl.slice(0, -1)
        : runtimeContext.sourceApiUrl,
      fetchApi: window.fetch.bind(window),
      middleware: [sigv4SignMiddleware],
    }),
  );
};

export const useDefaultApiClient = () => {
  const runtimeContext = useContext(RuntimeConfigContext);

  return useMemo(() => {
    return runtimeContext?.sourceApiUrl
      ? buildClient(runtimeContext)
      : undefined;
  }, [runtimeContext?.sourceApiUrl]);
};
