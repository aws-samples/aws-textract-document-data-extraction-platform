// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import {
  AggregateMetrics,
  DocumentMetadata,
  FormMetadata,
  FormSchema,
} from "@aws/document-extraction-platform-api-typescript-react-query-hooks";
import {
  Button,
  Column,
  ColumnLayout,
  Container,
  Grid,
  KeyValuePair,
  Stack,
  Tabs,
} from "aws-northstar";
import React, { useCallback, useEffect, useMemo, useState } from "react";
import { DocumentsTable } from "./documents-table";
import { FormsTable } from "./forms-table";
import {
  friendlyDuration,
  friendlyPercent,
  getMetricsForLastThreeMonths,
} from "../../api/metrics";
import { listAllPages } from "../../api/utils";
import { useDefaultApiClient } from "../../hooks/useDefaultApiClient";

export interface DashboardProps {}

/**
 * Default app content container for the "/" route…displays various metrics
 * about the processing of disclosure documents, along with a browseable view
 * of all documents that have been uploaded to the processing backend
 */
const Dashboard: React.FC<DashboardProps> = () => {
  const [dataLoaded, setDataLoaded] = useState<boolean>(false);
  const [formsLoaded, setFormsLoaded] = useState<boolean>(false);
  const [_, setDocumentsLoaded] = useState<boolean>(false);
  const [documentsLoaded, setSchemasLoaded] = useState<boolean>(false);
  const [schemas, setSchemas] = useState<FormSchema[]>([]);

  const [documents, setDocuments] = useState<DocumentMetadata[]>([]);
  const [forms, setForms] = useState<FormMetadata[]>([]);
  const [metrics, setMetrics] = useState<AggregateMetrics>();
  const tabHistoryKey = "dashboardTab";
  const defaultTab = "documents";

  const API = useDefaultApiClient()!;

  const fetchMetrics = useCallback(async () => {
    setMetrics(await getMetricsForLastThreeMonths(API));
  }, []);

  const fetchDocuments = useCallback(async () => {
    setDocumentsLoaded(false);
    const documentsResponse = await listAllPages(
      API.listDocuments.bind(API),
      "documents",
    );
    setDocuments(documentsResponse);
    setDocumentsLoaded(true);
  }, []);

  const fetchSchemas = useCallback(async () => {
    setSchemasLoaded(false);
    const schemasResponse = await listAllPages(
      API.listFormSchemas.bind(API),
      "schemas",
    );
    setSchemas(schemasResponse);
    setSchemasLoaded(true);
  }, []);

  const fetchForms = useCallback(async () => {
    setFormsLoaded(false);
    const formsResponse = await listAllPages(API.listForms.bind(API), "forms");
    setForms(formsResponse);
    setFormsLoaded(true);
  }, []);

  const fetchData = useCallback(async () => {
    setDataLoaded(false);
    await Promise.all([
      fetchDocuments(),
      fetchSchemas(),
      fetchForms(),
      fetchMetrics(),
    ]);
    setDataLoaded(true);
  }, []);

  const submitDocument = useCallback(async (file: File, schemaId: string) => {
    const { url, documentId, location } = await API.getDocumentUploadUrl({
      fileName: file.name,
      contentType: file.type,
    });

    await fetch(url, {
      method: "PUT",
      body: file,
    });
    await API.submitSourceDocument({
      submitSourceDocumentInput: {
        documentId,
        location,
        name: file.name,
        schemaId,
      },
    });
    // Start fetching documents but don't block returning from upload callback
    void (async () => fetchData())();
  }, []);

  useEffect(() => {
    fetchData().catch((err: any) => console.log(err));
  }, []);

  // tabs for the documents and forms views
  const tabs = useMemo(() => {
    return [
      {
        label: "Documents",
        id: defaultTab,
        content: (
          <DocumentsTable
            dataLoaded={documentsLoaded}
            reloadAction={fetchDocuments}
            documents={documents}
            upload={submitDocument}
            schemas={schemas}
          />
        ),
      },
      {
        label: "Forms",
        id: "forms",
        content: (
          <FormsTable
            forms={forms}
            reloadAction={fetchForms}
            dataLoaded={formsLoaded}
          />
        ),
      },
    ];
  }, [
    forms,
    documents,
    fetchDocuments,
    documentsLoaded,
    fetchForms,
    formsLoaded,
    fetchSchemas,
  ]);

  return (
    <Grid container spacing={1}>
      <Grid item xs={2}>
        {" "}
      </Grid>
      <Grid item xs={12}>
        <Container
          headingVariant="h2"
          title="Document Data Extraction Platform Dashboard"
          actionGroup={
            <>
              <Button
                variant="icon"
                icon={"refresh"}
                onClick={fetchData}
                loading={!dataLoaded}
              />
            </>
          }
        >
          <ColumnLayout>
            <Column key="column1">
              <Stack>
                <KeyValuePair
                  label="Documents Processed"
                  value={metrics?.totalProcessedDocumentCount ?? "-"}
                />
                <KeyValuePair
                  label="Forms Extracted"
                  value={metrics?.totalSuccessfulFormCount ?? "-"}
                />
              </Stack>
            </Column>
            <Column key="column2">
              <Stack>
                <KeyValuePair
                  label="Average Review Time"
                  value={friendlyDuration(
                    metrics?.averageReviewTimeMilliseconds,
                  )}
                />
              </Stack>
            </Column>
            <Column key="column3">
              <Stack>
                <KeyValuePair
                  label="Average Extraction Accuracy"
                  value={friendlyPercent(
                    metrics?.averageExtractionAccuracyDistance,
                  )}
                />
                <KeyValuePair
                  label="Average Extraction Confidence"
                  value={friendlyPercent(metrics?.averageConfidence)}
                />
              </Stack>
            </Column>
          </ColumnLayout>
        </Container>
        <Tabs
          onChange={(activeTabId: string) =>
            localStorage.setItem(tabHistoryKey, activeTabId)
          }
          activeId={localStorage.getItem(tabHistoryKey) ?? defaultTab}
          tabs={tabs}
          variant={"container"}
        />
      </Grid>
    </Grid>
  );
};

export default Dashboard;
