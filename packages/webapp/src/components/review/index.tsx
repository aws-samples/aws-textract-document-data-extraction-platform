// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import { Grid, LoadingIndicator } from "aws-northstar";
import React, { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { API } from "../../api/client";
import { FormReviewPanel } from "../form-review-panel";
import { FormMetadata, FormSchema } from "@aws/api-typescript-runtime";

export interface PDFFormReviewProps {
  readonly isReadOnly: boolean;
}

/**
 * Host page for the form content review UI
 */
const PDFFormReview: React.FC<PDFFormReviewProps> = (
  props: PDFFormReviewProps
) => {
  const [documentForm, setDocumentForm] = useState<FormMetadata>();
  const [formSchema, setFormSchema] = useState<FormSchema>();

  const { formId, documentId } = useParams<{
    documentId: string;
    formId: string;
  }>();

  const fetchFormAndSchema = useCallback(async () => {
    const form = await API.getDocumentForm({
      documentId,
      formId,
    });

    const schema = await API.getFormSchema({
      schemaId: form.schemaId,
    });

    setDocumentForm(form);
    setFormSchema(schema);
  }, []);

  useEffect(() => {
    void (async () => {
      // Initial fetch
      await fetchFormAndSchema();
    })();
  }, []);

  return (
    <Grid container spacing={1}>
      <Grid item xs={12}>
        {documentForm && formSchema ? (
          <FormReviewPanel
            documentForm={documentForm}
            formSchema={formSchema}
            isReadOnly={props.isReadOnly}
          />
        ) : (
          <LoadingIndicator />
        )}
      </Grid>
    </Grid>
  );
};

export default PDFFormReview;
