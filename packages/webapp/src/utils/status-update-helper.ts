// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { DefaultApi } from "@aws/document-extraction-platform-api-typescript-react-query-hooks";

/**
 * Update a form review status, suppressing any errors
 */
export const updateStatus = async (
  API: DefaultApi,
  documentId: string,
  formId: string,
  newStatus: string,
) => {
  try {
    await API.updateStatus({
      documentId,
      formId,
      updateStatusInput: { newStatus },
    });
  } catch (error) {}
};
