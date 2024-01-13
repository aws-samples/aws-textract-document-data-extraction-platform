// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import {
  DocumentMetadata,
  FormMetadata,
} from "@aws/document-extraction-platform-api-typescript-react-query-hooks";
import {
  Button,
  Column,
  ColumnLayout,
  Container,
  Grid,
  Inline,
  Link,
  LoadingIndicator,
  Table,
} from "aws-northstar";
import { Column as TableColumn } from "aws-northstar/components/Table/types";
import React, { useCallback, useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";

import { listAllPages } from "../../api/utils";
import { useDefaultApiClient } from "../../hooks/useDefaultApiClient";
import { updateStatus } from "../../utils/status-update-helper";
import { PdfViewer } from "../pdf/pdf-viewer";
import { ExtractionExecutionStatusIndicator } from "../status/extractionExecutionStatusIndicator";

export interface DocumentProps {}

/**
 * Detail page for a document
 */
export const Document: React.FC<DocumentProps> = () => {
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isLoadingForms, setIsLoadingForms] = useState<boolean>(true);
  const [document, setDocument] = useState<DocumentMetadata>();
  const [forms, setForms] = useState<FormMetadata[]>([]);
  const selectedForm = useRef<FormMetadata>();
  const [pageNumber, setPageNumber] = useState<number>(1);

  const { documentId } = useParams<{ documentId: string }>();

  const API = useDefaultApiClient()!;

  const formColumnDefinitions: TableColumn<any>[] = [
    {
      id: "formId",
      width: 220,
      Header: "Form",
      accessor: "formId",
      Cell: ({ value, row }) => {
        const link = `/view/${row.original.documentId}/${value}`;
        return (
          <Link href={link} underlineHover={true}>
            {row.original.documentName} {value}
          </Link>
        );
      },
    },
    {
      id: "status",
      width: 200,
      Header: "Status", // backlog/in review/reviewed
      accessor: "extractionExecution.status",
      Cell: ({ value, row }) => (
        <ExtractionExecutionStatusIndicator
          status={value}
          documentId={row.original.documentId}
          formId={row.original.formId}
          updateStatus={(docId, formId) =>
            updateStatus(API, docId, formId, "REVIEWING")
          }
          statusReason={row.original.extractionExecution.statusReason}
        />
      ),
    },
    {
      id: "startPageIndex",
      width: 100,
      Header: "Start Page",
      accessor: "startPageIndex",
      // Page index starts from 0, and page number starts from 1
      Cell: ({ value }) => value + 1,
    },
    {
      id: "endPageIndex",
      width: 100,
      Header: "End Page",
      accessor: "endPageIndex",
      // Page index starts from 0, and page number starts from 1
      Cell: ({ value }) => value + 1,
    },
  ];

  const fetchForms = useCallback(async () => {
    setIsLoadingForms(true);
    setForms(
      await listAllPages(API.listDocumentForms.bind(API), "forms", {
        documentId: documentId!,
      }),
    );
    setIsLoadingForms(false);
  }, [documentId]);

  const fetchDocumentAndForms = useCallback(async () => {
    setIsLoading(true);
    const [doc] = await Promise.all([
      API.getDocument({ documentId: documentId! }),
      fetchForms(),
    ]);
    setDocument(doc);
    setIsLoading(false);
  }, []);

  useEffect(() => {
    void (async () => {
      await fetchDocumentAndForms();
    })();
  }, []);

  const onSelectForm = useCallback(
    (form: FormMetadata) => {
      selectedForm.current = form;
      // Page index is 0-based
      setPageNumber(form.startPageIndex + 1);
    },
    [selectedForm, setPageNumber],
  );

  return isLoading || !document ? (
    <LoadingIndicator />
  ) : (
    <>
      <Container title={`Viewing Document ${document.name}`}>
        <ColumnLayout>
          <Column>
            <Grid container spacing={1}>
              <Grid item xs={12}>
                <Container
                  style={{
                    marginBottom: "0px",
                    boxShadow: "none",
                  }}
                >
                  <Table
                    actionGroup={
                      <Inline>
                        <Button
                          variant="icon"
                          icon={"refresh"}
                          onClick={async () => {
                            await fetchForms();
                          }}
                          loading={isLoadingForms}
                        />
                      </Inline>
                    }
                    onSelectionChange={(event) => {
                      if (event[0]?.formId !== selectedForm.current?.formId) {
                        onSelectForm(event[0]);
                      }
                    }}
                    getRowId={(row) => row.formId}
                    selectedRowIds={
                      selectedForm.current ? [selectedForm.current.formId] : []
                    }
                    tableTitle="Classified Forms"
                    columnDefinitions={formColumnDefinitions}
                    items={forms}
                    loading={isLoadingForms}
                    disableGroupBy={true}
                    disableSettings={true}
                    disablePagination={true}
                    disableFilters={true}
                    disableSortBy={true}
                    disableRowSelect={false}
                    multiSelect={false}
                    rowCount={forms.length}
                    defaultPageSize={forms.length}
                  />
                </Container>
              </Grid>
            </Grid>
          </Column>
          <Column>
            <PdfViewer
              url={document.url!}
              pageNumber={pageNumber}
              setPageNumber={setPageNumber}
            />
          </Column>
        </ColumnLayout>
      </Container>
    </>
  );
};
