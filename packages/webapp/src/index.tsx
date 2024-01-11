/*! Copyright [Amazon.com](http://amazon.com/), Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0 */
import React from "react";
import { createRoot } from "react-dom/client";
import RuntimeContextProvider from "./components/runtime-context";
import App from "./App";

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <RuntimeContextProvider>
      <App />
    </RuntimeContextProvider>
  </React.StrictMode>
);
