// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { DefaultApi } from "@aws/document-extraction-platform-api-typescript-react-query-hooks";
import humanizeDuration from "humanize-duration";

const THREE_MONTHS_IN_MILLIS = 3 * 31 * 24 * 60 * 60 * 1000;

export const friendlyDuration = (millis?: number) =>
  millis !== undefined
    ? humanizeDuration(millis, { largest: 2, round: true })
    : "-";
export const friendlyPercent = (percent?: number) =>
  percent !== undefined ? `${percent.toFixed(0)}%` : "-";

export const getMetricsForLastThreeMonths = (api: DefaultApi) =>
  api.getMetrics({
    startTimestamp: new Date(Date.now() - THREE_MONTHS_IN_MILLIS).toISOString(),
    endTimestamp: new Date().toISOString(),
  });
