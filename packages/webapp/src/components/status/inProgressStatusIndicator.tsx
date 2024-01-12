// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import InfoOutlinedIcon from "@material-ui/icons/InfoOutlined";
import { Box, NORTHSTAR_COLORS } from "aws-northstar";
import React from "react";

export interface InProgressStatusIndicatorProps {
  readonly label: string;
}

/**
 * A status indicator component for something in progress, not yet requiring attention
 */
export const InProgressStatusIndicator: React.FC<
  InProgressStatusIndicatorProps
> = ({ label }) => {
  return (
    <Box style={{ color: NORTHSTAR_COLORS.GREY_700, display: "flex" }}>
      <InfoOutlinedIcon fontSize="small" />
      <span style={{ marginLeft: 2 }}>{label}</span>
    </Box>
  );
};
