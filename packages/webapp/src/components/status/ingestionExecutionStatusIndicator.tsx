// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { ExecutionStatus } from "@aws/document-extraction-platform-api-typescript-react-query-hooks";
import { Popover, StatusIndicator } from "aws-northstar";
import React from "react";
import { InProgressStatusIndicator } from "./inProgressStatusIndicator";

export interface IngestionExecutionStatusIndicatorProps {
  readonly status: ExecutionStatus;
  readonly statusReason?: string;
}

/**
 * Display the status of document ingestion
 */
export const IngestionExecutionStatusIndicator: React.FC<
  IngestionExecutionStatusIndicatorProps
> = ({ status, statusReason }) => {
  switch (status) {
    case "IN_PROGRESS":
      return <InProgressStatusIndicator label="Classifying" />;
    case "SUCCEEDED":
      return (
        <StatusIndicator statusType="positive">Classified</StatusIndicator>
      );
    default:
      const indicator = (
        <StatusIndicator statusType="negative">Failed</StatusIndicator>
      );
      return (
        <>
          {statusReason ? (
            <Popover
              position="bottom"
              size="medium"
              header="Extraction Failed"
              content={statusReason}
            >
              {indicator}
            </Popover>
          ) : (
            indicator
          )}
        </>
      );
  }
};
