// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { LoadingIndicator, Alert } from "aws-northstar";
import React, { createContext, useEffect, useState } from "react";

export interface RuntimeContext {
  readonly region: string;
  readonly userPoolId: string;
  readonly userPoolWebClientId: string;
  readonly identityPoolId: string;
  readonly [additionalProps: string]: string;
}

/**
 * Context for storing the runtimeContext.
 */
export const RuntimeConfigContext = createContext<RuntimeContext | undefined>(
  undefined,
);

const RuntimeContextProvider: React.FC<any> = ({ children }) => {
  const [runtimeContext, setRuntimeContext] = useState<
    RuntimeContext | undefined
  >();
  const [error, setError] = useState<string | undefined>();

  useEffect(() => {
    fetch("/runtime-config.json")
      .then((response) => {
        return response.json();
      })
      .then((runtimeCtx) => {
        if (
          runtimeCtx.region &&
          runtimeCtx.userPoolId &&
          runtimeCtx.userPoolWebClientId &&
          runtimeCtx.identityPoolId
        ) {
          setRuntimeContext(runtimeCtx as RuntimeContext);
        } else {
          setError(
            "runtime-config.json should have region, userPoolId, userPoolWebClientId & identityPoolId.",
          );
        }
      })
      .catch(() => {
        setError("No runtime-config.json detected");
      });
  }, [setRuntimeContext]);

  return error ? (
    <Alert type="error">{error}</Alert>
  ) : runtimeContext ? (
    <RuntimeConfigContext.Provider value={runtimeContext}>
      {children}
    </RuntimeConfigContext.Provider>
  ) : (
    <LoadingIndicator size="large" />
  );
};

export default RuntimeContextProvider;
