/*! Copyright [Amazon.com](http://amazon.com/), Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0 */
import { NorthStarThemeProvider } from "@aws-northstar/ui";
import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import Auth from "./components/Auth";
import DefaultApiClientProvider from "./components/DefaultApi";
import RuntimeContextProvider from "./components/RuntimeContext";
import App from "./layouts/App";

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <NorthStarThemeProvider>
      <BrowserRouter>
        <RuntimeContextProvider>
          <Auth>
            <DefaultApiClientProvider>
              <App />
            </DefaultApiClientProvider>
          </Auth>
        </RuntimeContextProvider>
      </BrowserRouter>
    </NorthStarThemeProvider>
  </React.StrictMode>,
);
