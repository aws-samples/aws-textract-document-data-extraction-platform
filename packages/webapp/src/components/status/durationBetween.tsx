// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { StatusTransition } from "@aws/document-extraction-platform-api-typescript-react-query-hooks";
import humanizeDuration from "humanize-duration";
import React, { useMemo } from "react";

export interface DurationBetweenProps {
  fromStatuses: string[];
  toStatuses: string[];
  statusTransitionLog: StatusTransition[];
}

/**
 * Displays a human readable duration between the transition between the given statuses
 */
export const DurationBetween: React.FC<DurationBetweenProps> = ({
  fromStatuses,
  toStatuses,
  statusTransitionLog,
}) => {
  const toStatusesSet = useMemo(() => new Set(toStatuses), [toStatuses]);
  const fromStatusesSet = useMemo(() => new Set(fromStatuses), [fromStatuses]);

  // Find the first occurrence of the "from" status
  const fromTimestamp = useMemo(
    () =>
      statusTransitionLog.find(({ status }) => fromStatusesSet.has(status))
        ?.timestamp,
    [fromStatusesSet, statusTransitionLog],
  );

  // Find the last occurrence of the "to" status
  const toTimestamp = useMemo(
    () =>
      statusTransitionLog
        .reverse()
        .find(({ status }) => toStatusesSet.has(status))?.timestamp,
    [toStatusesSet, statusTransitionLog],
  );

  return (
    <>
      {fromTimestamp && toTimestamp
        ? humanizeDuration(
            new Date(toTimestamp).getTime() - new Date(fromTimestamp).getTime(),
            { largest: 2, round: true },
          )
        : "N/A"}
    </>
  );
};
