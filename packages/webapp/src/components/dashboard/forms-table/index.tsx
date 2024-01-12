// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import {
  FormMetadata,
  FormReviewWorkflowTag,
  StatusTransition,
} from "@aws/document-extraction-platform-api-typescript-react-query-hooks";
import { Badge, Button, Inline, Link } from "aws-northstar";
import Table from "aws-northstar/components/Table";
import { Column as TableColumn } from "aws-northstar/components/Table/types";
import Grid from "aws-northstar/layouts/Grid";
import React, { useState, useEffect } from "react";

import { listAllPages } from "../../../api/utils";
import { useDefaultApiClient } from "../../../hooks/useDefaultApiClient";
import { tagIdsToTags } from "../../../utils/review-tags-helper";
import { updateStatus } from "../../../utils/status-update-helper";
import { DurationBetween } from "../../status/durationBetween";
import { ExtractionExecutionStatusIndicator } from "../../status/extractionExecutionStatusIndicator";

export interface FormsTableProps {
  readonly dataLoaded?: boolean;
  readonly forms: FormMetadata[];
  readonly reloadAction?: any;
}

export const FormsTable: React.FC<FormsTableProps> = ({
  dataLoaded,
  forms,
  reloadAction,
}) => {
  const [availableReviewTags, setAvailableReviewTags] =
    useState<FormReviewWorkflowTag[]>();

  const formListColumns: TableColumn<any>[] = [
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
      id: "schema",
      width: 120,
      Header: "Schema",
      accessor: "schemaId",
    },
    {
      id: "updatedTimestamp",
      width: 150,
      Header: "Last Updated",
      accessor: "updatedTimestamp",
      Cell: ({ value }) => <>{new Date(value).toLocaleString()}</>,
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
          updateStatus={(documentId, formId) =>
            updateStatus(API, documentId, formId, "REVIEWING")
          }
          statusReason={row.original.extractionExecution.statusReason}
        />
      ),
    },
    {
      id: "tags",
      width: 250,
      Header: "Tags",
      accessor: "tags",
      // @ts-ignore
      Cell: ({ value, row }) => (
        <>
          {tagIdsToTags(row.original.tags, availableReviewTags)?.map(
            (tag: any) => <Badge key={tag.tagId} content={tag.tagText} />,
          )}
        </>
      ),
    },
    {
      id: "reviewer",
      width: 100,
      Header: "Reviewer",
      accessor: "statusTransitionLog",
      Cell: ({ value }: { value: StatusTransition[] }) => (
        <>
          {value.find(({ status }) => status === "REVIEWED")?.actingUser ||
            value.find(({ status }) => status === "REVIEWING")?.actingUser ||
            "N/A"}
        </>
      ),
    },
    {
      id: "extractionTime",
      width: 100,
      Header: "Data Extraction Time",
      accessor: "statusTransitionLog",
      Cell: ({ value }) => (
        <DurationBetween
          fromStatuses={["CLASSIFICATION_SUCCEEDED"]}
          toStatuses={["READY_FOR_REVIEW", "EXTRACTION_FAILED"]}
          statusTransitionLog={value}
        />
      ),
    },
    {
      id: "waitTime",
      width: 100,
      Header: "Time in Queue",
      accessor: "statusTransitionLog",
      Cell: ({ value }) => (
        <DurationBetween
          fromStatuses={["READY_FOR_REVIEW"]}
          toStatuses={["REVIEWING"]}
          statusTransitionLog={value}
        />
      ),
    },
    {
      id: "reviewTime",
      width: 100,
      Header: "Time in Review",
      accessor: "statusTransitionLog",
      Cell: ({ value }) => (
        <DurationBetween
          fromStatuses={["REVIEWING"]}
          toStatuses={["REVIEWED"]}
          statusTransitionLog={value}
        />
      ),
    },
  ];

  const API = useDefaultApiClient()!;

  useEffect(() => {
    void (async () => {
      const tags = await listAllPages(
        API.listFormReviewWorkflowTags.bind(API),
        "tags",
      );
      setAvailableReviewTags(tags);
    })();
  }, []);

  const actionGroup = (
    <Inline>
      {reloadAction ? (
        <Button
          variant="icon"
          icon={"refresh"}
          onClick={async () => {
            reloadAction();
          }}
          loading={!dataLoaded}
        />
      ) : (
        <></>
      )}
    </Inline>
  );

  return (
    <Grid container spacing={1}>
      <Grid item xs={12}>
        <Table
          tableTitle={"Extracted Forms"}
          actionGroup={actionGroup}
          columnDefinitions={formListColumns}
          items={forms}
          loading={!dataLoaded}
          multiSelect={false}
          disableGroupBy={true}
          disableSettings={true}
          disableFilters={false}
          disableRowSelect={true}
          disableSortBy={false}
        />
      </Grid>
    </Grid>
  );
};
