/**********************************************************************************************************************
 *  Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                           *
 *                                                                                                                    *
 *  Licensed under the Amazon Software License (the "License"). You may not use this file except in compliance        *
 *  with the License. A copy of the License is located at                                                             *
 *                                                                                                                    *
 *     http://aws.amazon.com/asl/                                                                                     *
 *                                                                                                                    *
 *  or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES *
 *  OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions    *
 *  and limitations under the License.                                                                                *
 **********************************************************************************************************************/
import { DocumentMetadata, FormSchema } from '@aws/api-typescript';
import { Button, Inline, Link, Modal, Select } from 'aws-northstar';
import FileUpload from 'aws-northstar/components/FileUpload';
import { SelectOption } from 'aws-northstar/components/Select/types';
import Table from 'aws-northstar/components/Table';
import { Column as TableColumn } from 'aws-northstar/components/Table/types';
import Grid from 'aws-northstar/layouts/Grid';
import React, { useCallback, useState } from 'react';
import { IngestionExecutionStatusIndicator } from '../../status/ingestionExecutionStatusIndicator';

const documentListColumns: TableColumn<any>[] = [
  {
    id: 'name',
    width: 200,
    Header: 'Name',
    accessor: 'name',
    Cell: ({ value, row }) => <Link href={`/view/${row.original.documentId}`}>{value}</Link>,
  },
  {
    id: 'createdBy',
    width: 150,
    Header: 'Uploaded By',
    accessor: 'createdBy',
  },
  {
    id: 'createdTimestamp',
    width: 150,
    Header: 'Uploaded At',
    accessor: 'createdTimestamp',
    Cell: ({ value }) => <>{new Date(value).toLocaleString()}</>,
  },
  {
    id: 'status',
    width: 150,
    Header: 'Status', // backlog/in review/reviewed
    accessor: 'ingestionExecution.status',
    Cell: ({ value, row }) => <IngestionExecutionStatusIndicator status={value} statusReason={row.original.ingestionExecution.statusReason} />,
  },
  {
    id: 'numberOfPages',
    width: 100,
    Header: 'Pages',
    accessor: 'numberOfPages',
  },
];

export interface DocumentsTableProps {
  readonly dataLoaded?: boolean;
  readonly documents: DocumentMetadata[];
  readonly upload: (file: File, schemaId: string) => Promise<void>;
  readonly schemas: FormSchema[];
  readonly reloadAction?: any;
}

export const DocumentsTable: React.FC<DocumentsTableProps> = ({ dataLoaded, documents, upload, schemas, reloadAction }) => {
  const [isUploadModalVisible, setIsUploadModalVisible] = useState<boolean>(false);
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
      {reloadAction ?
        <Button
          variant="icon"
          icon={'refresh'}
          onClick={async () => {
            await reloadAction();
          }}
          loading={!dataLoaded}
        /> : <></>}
    </Inline>
  );

  return (
    <>
      <Modal title='Upload a Document' visible={isUploadModalVisible} onClose={() => setIsUploadModalVisible(false)}>
        <h4>Select the schema of the document you want to upload</h4>
        <Select
          placeholder="Choose a schema type"
          label="Choose a schema type"
          options={options}
          onFocus={onFocus}
          selectedOption={selectedOption}
          onChange={(event) => setSelectedOption({ value: event.target.value } as any)}
        />
        <br></br><br></br>
        <FileUpload
          accept=".pdf"
          label="Select Document"
          description="A document must only contain one form and not multiple forms."
          controlId="upload"
          onChange={(files) => files.length > 0 && setFile(files[0] as File)}
          multiple={false}
        />
        <Button disabled={!file && !selectedOption} variant="primary" onClick={doUpload} loading={isUploading}>Upload</Button>
      </Modal>
      <Grid container spacing={1}>
        <Grid item xs={12}>
          <Table
            tableTitle={'Uploaded Documents'}
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
