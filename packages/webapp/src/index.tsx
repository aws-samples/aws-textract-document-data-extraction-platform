// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import Amplify from 'aws-amplify';
import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const { region, userPoolId, userPoolWebClientId, identityPoolId } =
  // @ts-ignore
  window.runtimeConfig;

Amplify.configure({
  Auth: {
    region: region,
    userPoolId: userPoolId,
    userPoolWebClientId: userPoolWebClientId,
    identityPoolId: identityPoolId,
  },
});

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root'),
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
