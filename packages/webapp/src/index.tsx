// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import RuntimeContextProvider from "./components/runtime-context";

ReactDOM.render(
  <React.StrictMode>
    <RuntimeContextProvider>
      <App />
    </RuntimeContextProvider>
  </React.StrictMode>,
  document.getElementById("root"),
);
