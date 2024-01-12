// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import {
  FormJSONSchema,
  FormSchema,
  AggregateMetrics,
  CreateFormSchemaRequest,
} from "@aws/document-extraction-platform-api-typescript-react-query-hooks";
import {
  Alert,
  Button,
  FormField,
  Grid,
  Inline,
  Input,
  Modal,
} from "aws-northstar";
import Table, { Column as TableColumn } from "aws-northstar/components/Table";
import React, { useCallback, useEffect, useState } from "react";
import { ModalButtons } from "./modal-buttons";
import { SchemaEditor } from "./schema-editor";

import {
  friendlyPercent,
  getMetricsForLastThreeMonths,
} from "../../api/metrics";
import { listAllPages } from "../../api/utils";
import { useDefaultApiClient } from "../../hooks/useDefaultApiClient";
import { stringifySchema } from "../../utils/review-panel/schema-helper";

export interface DocumentSchemaProps {}

const SCHEMA_TEMPLATE: FormJSONSchema = {
  description: "",
  typeOf: "object",
  properties: {
    myFormField: {
      title: "My Form Field",
      typeOf: "string",
      order: 1,
      extractionMetadata: {
        formKey: "Key for this form field as present in the document",
        tablePosition: 1,
        rowPosition: 1,
        columnPosition: 1,
        textractQuery: "What is my form field?",
      },
    },
  },
};

/**
 * Default app content container for the "/" route…displays various metrics
 * about the processing of disclosure documents, along with a browseable view
 * of all documents that have been uploaded to the processing backend
 * @returns Component for creating editing and deleting document schemas.
 */
const DocumentSchemas: React.FC<DocumentSchemaProps> = () => {
  const [dataLoaded, setDataLoaded] = useState<boolean>(false);
  const [selectedRow, setSelectedRow] = useState<FormSchema>();
  const [schemas, setSchemas] = useState<FormSchema[]>([]);
  const [metrics, setMetrics] = useState<AggregateMetrics>();
  const [isSchemaModalVisible, setIsSchemaModalVisible] =
    useState<boolean>(false);
  const [isSubmittingSchema, setIsSubmittingSchema] = useState<boolean>(false);
  const [isSubmittingAddSchema, setIsSubmittingAddSchema] =
    useState<boolean>(false);
  const [isAddSchemaModalVisible, setIsAddSchemaModalVisible] =
    useState<boolean>(false);
  let [newSchema, setNewSchema] = useState<string>("");
  let [addNewSchema, setAddNewSchema] = useState<string>("");
  let [formTitle, setFormTitle] = useState<string>("");
  let [formDesc, setFormDesc] = useState<string>("");
  let [errorMessage, setErrorMessage] = useState<string | undefined>();

  const API = useDefaultApiClient()!;

  const fetchSchemas = useCallback(async () => {
    setDataLoaded(false);
    const [schemasResponse, metricsResponse] = await Promise.all([
      listAllPages(API.listFormSchemas.bind(API), "schemas"),
      getMetricsForLastThreeMonths(API),
    ]);
    setSchemas(schemasResponse);
    setMetrics(metricsResponse);
    setDataLoaded(true);
  }, []);

  useEffect(() => {
    void (async () => {
      // Initial fetch
      await fetchSchemas();
    })();
  }, []);

  const actionGroup = (
    <Inline>
      <Button disabled={!selectedRow} onClick={async () => deleteSchema()}>
        Delete
      </Button>
      <Button
        disabled={!selectedRow}
        onClick={() => {
          setNewSchema(stringifySchema(selectedRow?.schema || {}));
          setIsSchemaModalVisible(true);
        }}
      >
        View/Edit
      </Button>
      <Button
        variant="primary"
        onClick={() => {
          setAddNewSchema(stringifySchema(SCHEMA_TEMPLATE));
          setIsAddSchemaModalVisible(true);
          setErrorMessage(undefined);
          setErrorMessage("");
        }}
      >
        Add
      </Button>
      <Button
        variant="icon"
        icon="refresh"
        onClick={async () => fetchSchemas()}
      />
    </Inline>
  );

  const schemaListColumns: TableColumn<any>[] = [
    {
      id: "title",
      width: 120,
      Header: "Name",
      accessor: "title",
    },
    {
      id: "schemaId",
      width: 150,
      Header: "Id",
      accessor: "schemaId",
    },
    {
      id: "updatedBy",
      width: 150,
      Header: "Updated By",
      accessor: "updatedBy",
    },
    {
      id: "updatedTimestamp",
      width: 150,
      Header: "Last Updated",
      accessor: "updatedTimestamp",
      Cell: ({ value }) => <>{new Date(value).toLocaleString()}</>,
    },
    {
      id: "accuracyPercent",
      width: 100,
      Header: "Average Accuracy",
      accessor: "schemaId",
      Cell: ({ value }) => (
        <>
          {friendlyPercent(
            metrics?.bySchemaId[value]?.averageExtractionAccuracyDistance,
          )}
        </>
      ),
    },
  ];

  const deleteSchema = useCallback(async () => {
    await API.deleteFormSchema({ schemaId: selectedRow!.schemaId });
    await fetchSchemas();
  }, [selectedRow, fetchSchemas]);

  const updateSchema = useCallback(async () => {
    let toBeUpdatedSchema = await API.getFormSchema({
      schemaId: selectedRow!.schemaId,
    });
    let schemasResponse;

    try {
      const parsedSchema: FormJSONSchema = JSON.parse(newSchema);
      toBeUpdatedSchema.schema = parsedSchema;
      schemasResponse = await API.updateFormSchema({
        schemaId: selectedRow!.schemaId,
        formSchema: toBeUpdatedSchema!,
      });
    } catch (error: any) {
      setIsSubmittingSchema(false);
      setErrorMessage("Could not update schema. " + error.message);
    }

    if (schemasResponse) {
      setIsSubmittingSchema(false);
      setIsSchemaModalVisible(false);
    }
  }, [newSchema, selectedRow]);

  const submitSchema = useCallback(async () => {
    setIsSubmittingSchema(true);
    await updateSchema();
    await fetchSchemas();
  }, [updateSchema, fetchSchemas]);

  const handleSubmit = useCallback(async () => {
    setIsSubmittingAddSchema(true);
    let schemasResponse;
    let parsedSchema: FormJSONSchema = {};

    try {
      parsedSchema = JSON.parse(addNewSchema);
      let input = {
        formSchemaInput: {
          title: formTitle,
          description: formDesc,
          schema: parsedSchema,
        },
      } as CreateFormSchemaRequest;
      schemasResponse = await API.createFormSchema(input);
    } catch (error: any) {
      setIsSubmittingAddSchema(false);
      setErrorMessage("Could not create schema. " + error.message);
    }

    if (schemasResponse) {
      await fetchSchemas();
      setIsSubmittingAddSchema(false);
      setIsSubmittingAddSchema(false);
      setIsAddSchemaModalVisible(false);
    }
  }, [formTitle, formDesc, addNewSchema, fetchSchemas]);

  const cancelSubmit = () => {
    setIsSubmittingSchema(false);
    setIsSchemaModalVisible(false);
  };

  const cancelAddSubmit = () => {
    setIsSubmittingAddSchema(false);
    setIsAddSchemaModalVisible(false);
  };

  return (
    <>
      <Modal
        width="70%"
        title={selectedRow?.title || ""}
        visible={isSchemaModalVisible}
        onClose={() => {
          setIsSchemaModalVisible(false);
          setIsSubmittingSchema(false);
        }}
      >
        {errorMessage && (
          <div style={{ marginBottom: 20 }}>
            <Alert
              type="error"
              dismissible={true}
              buttonText="Dismiss"
              onButtonClick={() => {
                setErrorMessage(undefined);
              }}
              header="Error"
            >
              {errorMessage}
            </Alert>
          </div>
        )}
        <SchemaEditor
          jsonSchema={newSchema}
          onChange={(e) => setNewSchema(e)}
        />
        <br />
        <ModalButtons
          loading={isSubmittingSchema}
          cancelOnClick={cancelSubmit}
          submitOnClick={submitSchema}
        />
      </Modal>

      <Modal
        width="70%"
        title="Add new schema"
        visible={isAddSchemaModalVisible}
        onClose={() => {
          setIsAddSchemaModalVisible(false);
          setIsSubmittingAddSchema(false);
        }}
      >
        {errorMessage && (
          <div style={{ marginBottom: 20 }}>
            <Alert
              type="error"
              dismissible={true}
              buttonText="Dismiss"
              onButtonClick={() => {
                setErrorMessage(undefined);
                setNewSchema(stringifySchema(selectedRow?.schema || {}));
              }}
              header="Error"
            >
              {errorMessage}
            </Alert>
          </div>
        )}
        <FormField
          label="Title"
          controlId="schemaFormName"
          hintText="This must exactly match the title on the first page of a corresponding form"
        >
          <Input
            type="text"
            controlId="schemaFormName"
            onChange={(e) => setFormTitle(e)}
          />
        </FormField>

        <FormField
          label="Description"
          controlId="schemaFormDescription"
          hintText="(Optional)"
        >
          <Input
            type="text"
            controlId="schemaFormDescription"
            onChange={(e) => setFormDesc(e)}
          />
        </FormField>

        <h1>Document Definition JSON</h1>
        <SchemaEditor
          jsonSchema={addNewSchema}
          onChange={(e: any) => setAddNewSchema(e)}
        />
        <br />
        <ModalButtons
          loading={isSubmittingAddSchema}
          cancelOnClick={cancelAddSubmit}
          submitOnClick={handleSubmit}
        />
      </Modal>

      <Grid container spacing={1}>
        <Grid item xs={2}>
          {" "}
        </Grid>
        <Grid item xs={12}>
          <Table
            tableTitle={"Document Schemas"}
            actionGroup={actionGroup}
            columnDefinitions={schemaListColumns}
            items={schemas}
            loading={!dataLoaded}
            multiSelect={false}
            disableGroupBy={true}
            disableSettings={true}
            disableFilters={false}
            disableRowSelect={false}
            disableSortBy={false}
            getRowId={(row) => row.schemaId}
            selectedRowIds={selectedRow ? [selectedRow.schemaId] : []}
            onSelectionChange={(event) => setSelectedRow(event[0])}
          />
        </Grid>
      </Grid>
    </>
  );
};

export default DocumentSchemas;
