// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { ExtractionExecutionStatus } from "@aws/document-extraction-platform-api-typescript-react-query-hooks";
import {
  Inline,
  Link,
  NORTHSTAR_COLORS,
  Popover,
  StatusIndicator,
} from "aws-northstar";
import Icon from "aws-northstar/components/Icon";
import React from "react";
import { InProgressStatusIndicator } from "./inProgressStatusIndicator";

export interface ExtractionExecutionStatusIndicatorProps {
  readonly status: ExtractionExecutionStatus;
  readonly statusReason?: string;
  readonly documentId: string;
  readonly formId: string;
  updateStatus: (documentId: string, formId: string) => void;
}

/**
 * Display the status of form data extraction
 */
export const ExtractionExecutionStatusIndicator: React.FC<
  ExtractionExecutionStatusIndicatorProps
> = ({ status, statusReason, documentId, formId, updateStatus }) => {
  const link = `/review/${documentId}/${formId}`;

  switch (status) {
    case "NOT_STARTED":
    case "IN_PROGRESS":
      return <InProgressStatusIndicator label="Extracting Data" />;
    case "READY_FOR_REVIEW":
      return (
        <>
          <Inline spacing="xs">
            <Icon
              name="AssignmentLateSharp"
              fontSize="small"
              variant="Outlined"
              htmlColor={NORTHSTAR_COLORS.ORANGE}
            />
            <Link
              href={link}
              underlineHover={true}
              onClick={async () => updateStatus(documentId, formId)}
            >
              Ready for Review
            </Link>
          </Inline>
        </>
      );
    case "REVIEWING":
      return (
        <>
          <Inline spacing="xs">
            <Icon
              name="AssignmentSharp"
              fontSize="small"
              variant="Outlined"
              htmlColor={NORTHSTAR_COLORS.BLUE}
            />
            <Link href={link} underlineHover={true}>
              In Review
            </Link>
          </Inline>
        </>
      );
    case "REVIEWED":
      return (
        <>
          <Inline spacing="xs">
            <Icon
              name="AssignmentTurnedInSharp"
              fontSize="small"
              variant="Outlined"
              htmlColor={NORTHSTAR_COLORS.GREEN}
            />
            <Link
              href={link}
              underlineHover={true}
              onClick={async () => updateStatus(documentId, formId)}
            >
              Review Complete
            </Link>
          </Inline>
        </>
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
