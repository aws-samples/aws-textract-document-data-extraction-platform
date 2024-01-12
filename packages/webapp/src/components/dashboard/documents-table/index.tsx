// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import {
  DocumentMetadata,
  FormSchema,
} from "@aws/document-extraction-platform-api-typescript-react-query-hooks";
import { Button, Inline, Link, Modal, Select } from "aws-northstar";
import FileUpload from "aws-northstar/components/FileUpload";
import { SelectOption } from "aws-northstar/components/Select/types";
import Table from "aws-northstar/components/Table";
import { Column as TableColumn } from "aws-northstar/components/Table/types";
import Grid from "aws-northstar/layouts/Grid";
import React, { useCallback, useState } from "react";

const documentListColumns: TableColumn<DocumentMetadata>[] = [
  {
    id: "name",
    width: 200,
    Header: "Name",
    accessor: "name",
    Cell: ({ value, row }) => (
      <Link href={`/view/${row.original.documentId}`}>{value}</Link>
    ),
  },
  {
    id: "createdBy",
    width: 150,
    Header: "Uploaded By",
    accessor: "createdBy",
  },
  {
    id: "createdTimestamp",
    width: 150,
    Header: "Uploaded At",
    accessor: "createdTimestamp",
    Cell: ({ value }) => <>{value ? new Date(value).toLocaleString() : "-"}</>,
  },
  {
    id: "numberOfPages",
    width: 100,
    Header: "Pages",
    accessor: "numberOfPages",
  },
];

export interface DocumentsTableProps {
  readonly dataLoaded?: boolean;
  readonly documents: DocumentMetadata[];
  readonly upload: (file: File, schemaId: string) => Promise<void>;
  readonly schemas: FormSchema[];
  readonly reloadAction?: any;
}

export const DocumentsTable: React.FC<DocumentsTableProps> = ({
  dataLoaded,
  documents,
  upload,
  schemas,
  reloadAction,
}) => {
  const [isUploadModalVisible, setIsUploadModalVisible] =
    useState<boolean>(false);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [file, setFile] = useState<File | undefined>();
  const [options, setOptions] = React.useState<SelectOption[]>([]);
  const [selectedOption, setSelectedOption] = React.useState<SelectOption>();

  const schemaOptions = schemas.map((schema) => {
    return {
      label: schema.schemaId,
      value: schema.schemaId,
    };
  });

  const onFocus = () => {
    setTimeout(() => {
      setOptions(schemaOptions);
    }, 1000);
  };

  const doUpload = useCallback(async () => {
    if (selectedOption) {
      setIsUploading(true);
      await upload(file!, selectedOption.value!);
      setIsUploading(false);
      setIsUploadModalVisible(false);
    }
  }, [file, selectedOption]);

  const actionGroup = (
    <Inline>
      <Button variant="primary" onClick={() => setIsUploadModalVisible(true)}>
        Upload
      </Button>
      {reloadAction ? (
        <Button
          variant="icon"
          icon={"refresh"}
          onClick={async () => {
            await reloadAction();
          }}
          loading={!dataLoaded}
        />
      ) : (
        <></>
      )}
    </Inline>
  );

  return (
    <>
      <Modal
        title="Upload a Document"
        visible={isUploadModalVisible}
        onClose={() => setIsUploadModalVisible(false)}
      >
        <h4>Select the schema of the document you want to upload</h4>
        <Select
          placeholder="Choose a schema type"
          label="Choose a schema type"
          options={options}
          onFocus={onFocus}
          selectedOption={selectedOption}
          onChange={(event) =>
            setSelectedOption({ value: event.target.value } as any)
          }
        />
        <br></br>
        <br></br>
        <FileUpload
          accept=".pdf"
          label="Select Document"
          description="A document must only contain one form and not multiple forms."
          controlId="upload"
          onChange={(files) => files.length > 0 && setFile(files[0] as File)}
          multiple={false}
        />
        <Button
          disabled={!file && !selectedOption}
          variant="primary"
          onClick={doUpload}
          loading={isUploading}
        >
          Upload
        </Button>
      </Modal>
      <Grid container spacing={1}>
        <Grid item xs={12}>
          <Table
            tableTitle={"Uploaded Documents"}
            actionGroup={actionGroup}
            columnDefinitions={documentListColumns}
            items={documents}
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
    </>
  );
};
