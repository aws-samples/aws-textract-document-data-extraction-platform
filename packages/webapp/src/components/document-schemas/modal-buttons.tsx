// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { Button } from "aws-northstar";
import React from "react";

export interface ModalButtonsProps {
  loading: boolean;
  cancelOnClick: () => void;
  submitOnClick: (e: any) => void;
}

/**
 * @param loading boolean to indicate if the form is loading
 * @param submitOnClick function to be called when the submit button is clicked
 * @param cancelOnClick function to be called when the cancel button is clicked
 * @returns Component that creates and styles the buttons that should be displayed in the modal footer.
 */
export const ModalButtons: React.FC<ModalButtonsProps> = ({
  loading,
  submitOnClick,
  cancelOnClick,
}) => {
  return (
    <div
      style={{
        display: "flex",
        float: "right",
        justifyContent: "space-between",
      }}
    >
      <Button variant="primary" onClick={cancelOnClick}>
        Cancel
      </Button>
      <Button variant="primary" onClick={submitOnClick} loading={loading}>
        Submit
      </Button>
    </div>
  );
};
