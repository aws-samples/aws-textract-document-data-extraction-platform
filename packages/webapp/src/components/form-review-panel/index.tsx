// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import {
  FormMetadata,
  FormSchema,
  FormReviewWorkflowTag,
} from "@aws/document-extraction-platform-api-typescript-react-query-hooks";
import {
  Alert,
  Badge,
  Box,
  Button,
  Checkbox,
  Column,
  ColumnLayout,
  Container,
  FormField,
  Heading,
  Inline,
  Input,
  Modal,
  Multiselect,
} from "aws-northstar";
import Table, { Row } from "aws-northstar/components/Table";
import { Column as TableColumn } from "aws-northstar/components/Table/types";
import Grid from "aws-northstar/layouts/Grid";
import _ from "lodash";
import React, {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { useHistory } from "react-router-dom";

import { listAllPages } from "../../api/utils";
import { useDefaultApiClient } from "../../hooks/useDefaultApiClient";
import {
  flattenFormSchema,
  FormValue,
  stringifyDataAccordingToSchema,
  stringifySchema,
} from "../../utils/review-panel/schema-helper";
import {
  ReviewMultiselectTagOption,
  tagIdsToTags,
} from "../../utils/review-tags-helper";
import { updateStatus } from "../../utils/status-update-helper";
import { SchemaEditor } from "../document-schemas/schema-editor";
import { DrawWrapper, PdfViewer } from "../pdf/pdf-viewer";

export interface FormReviewPanelProps {
  readonly documentForm: FormMetadata;
  readonly formSchema: FormSchema;
  readonly isReadOnly: boolean;
}

// transform a list of form review workflow tag objects into those consumed
// by the Multiselect component
export const tagsToMultiselectOptions = (
  tags: any,
): ReviewMultiselectTagOption[] => {
  return tags?.map((tag: any) => {
    return { label: tag.tagText, value: tag.tagId };
  });
};

// extract list of tag ids from a list of Multiselect component value objects
export const multiselectOptionsToTagIds = (options: any): string[] => {
  return options?.map((tag: any) => tag.value);
};

/**
 * Component to render a content review UI for a given form, rendering
 * the disclosure form PDF on the right of the UI and the textract
 * extracted content in a table on the left.
 */
export const FormReviewPanel: React.FC<FormReviewPanelProps> = ({
  documentForm,
  formSchema,
  isReadOnly,
}) => {
  const selectedFormField = useRef<FormValue>();
  const [showRawDataModal, setShowRawDataModal] = useState<boolean>(false);
  const [pageNumber, setPageNumber] = useState(1);
  const [isReviewComplete, setIsReviewComplete] = useState<boolean>(false);
  const [isSubmittingReview, setIsSubmittingReview] = useState<boolean>(false);
  const [showSuccessAlert, setShowSuccessAlert] = useState<boolean>(false);
  const [reviewTags, setReviewTags] = useState<ReviewMultiselectTagOption[]>();
  const [selectedReviewTags, setSelectedReviewTags] =
    useState<ReviewMultiselectTagOption[]>();
  const [availableReviewWorkflowTags, setAvailableReviewWorkflowTags] =
    useState<FormReviewWorkflowTag[]>();

  let [docForm, setDocForm] = useState<FormMetadata>(documentForm);

  const updateFormValues = (
    formValueList: FormValue[],
    row: Row<any>,
    e: string,
  ) => {
    formValueList
      .filter((x) => x.key === `${row.original.key}`)
      .map((f) => {
        _.update(f, "value", function () {
          return e;
        });
      });
  };

  // Ref used for us to draw on the page
  const drawRef = useRef<DrawWrapper>(() => {});

  // The form's extracted data is in the shape defined by the schema, flatten here for more intuitive review
  const flattenedFields = useMemo(() => flattenFormSchema(docForm), [docForm]);
  const [formValues, setFormValues] = useState<FormValue[]>(flattenedFields);

  const API = useDefaultApiClient()!;

  useEffect(() => {
    void (async () => {
      const tags = await listAllPages(
        API.listFormReviewWorkflowTags.bind(API),
        "tags",
      );
      setAvailableReviewWorkflowTags(tags);
      setReviewTags(tagsToMultiselectOptions(tags));
      setSelectedReviewTags(
        tagsToMultiselectOptions(tagIdsToTags(docForm?.tags, tags)),
      );
    })();
    setFormValues(formValues);
  }, [flattenedFields]);

  const drawBoundingBoxForSelectedRow = useCallback(() => {
    const field = selectedFormField.current;
    if (!drawRef.current || !field) {
      return;
    }
    drawRef.current((ctx, { width, height }) => {
      // Only draw the box if we're on the right page to display it
      if (field.page !== undefined && field.page + 1 === pageNumber) {
        ctx.fillStyle = "rgba(144, 238, 144, 0.5)";
        ctx.fillRect(
          field.boundingBox.left * width,
          field.boundingBox.top * height,
          field.boundingBox.width * width,
          field.boundingBox.height * height,
        );
      }
    });
  }, [drawRef, selectedFormField, pageNumber]);

  const onPageRenderSuccess = useCallback(() => {
    // Redraw the bounding box whenever we change page
    drawBoundingBoxForSelectedRow();
  }, [drawBoundingBoxForSelectedRow]);

  const onSelectRow = useCallback(
    (row) => {
      selectedFormField.current = row;

      if (!row) {
        return;
      }

      if (row.page !== undefined && row.page + 1 !== pageNumber) {
        // We've selected a row which has a box on a different page to the current page number, so jump to that page.
        // We return here since the page change is not immediate - rendering of the new page will then trigger drawing
        // the bounding box.
        setPageNumber(row.page + 1);
        return;
      }

      // Draw the bounding box for the selected row
      drawBoundingBoxForSelectedRow();
    },
    [pageNumber, selectedFormField, drawBoundingBoxForSelectedRow],
  );

  const onSelectionChange = useCallback(
    (event) => {
      if (event[0]?.key !== selectedFormField.current?.key) {
        onSelectRow(event[0]);
      }
    },
    [onSelectRow, selectedFormField],
  );

  const formFields: TableColumn<any>[] = useMemo(
    () => [
      {
        id: "fieldName",
        width: 200,
        Header: "Name",
        accessor: "key",
        Cell: ({ value }) => <Box marginTop={1}>{value}</Box>,
      },
      {
        id: "fieldValue",
        width: 300,
        Header: "Value",
        accessor: "value",
        Cell: ({ value, row }) => {
          if (isReadOnly) {
            return <Box marginTop={1}>{value}</Box>;
          }
          return (
            <FormField stretch={true} controlId={row.id}>
              <Input
                type="text"
                controlId={row.id}
                value={value ? value : ""}
                onFocus={() => {
                  onSelectRow(row.original);
                }}
                onChange={(e) => {
                  _.set(docForm, `extractedData[${row.original.key}]`, e);
                  setDocForm(docForm);
                  updateFormValues(formValues, row, e);
                }}
              />
            </FormField>
          );
        },
      },
      {
        id: "confidence",
        width: 100,
        Header: "Confidence",
        accessor: "confidence",
        Cell: ({ value }) => (
          <Box marginTop={1}>{Number(value).toFixed(2) + " %"}</Box>
        ),
      },
      {
        id: "method",
        width: 100,
        Header: "Extraction Method",
        accessor: "extractionMethod",
        Cell: ({ value }) => <Box marginTop={1}>{value}</Box>,
      },
    ],
    [isReadOnly, onSelectRow, setDocForm, updateFormValues],
  );

  const history = useHistory();

  const updateExtractedData = async () => {
    setIsSubmittingReview(true);
    setShowSuccessAlert(false);
    const reviewNotes = (
      document.getElementById("reviewNotesTextArea") as HTMLInputElement
    ).value;
    await API.updateFormReview({
      updateFormInput: {
        extractedData: docForm.extractedData,
        ...(reviewNotes && reviewNotes.length > 0
          ? { notes: reviewNotes }
          : {}),
        ...(selectedReviewTags
          ? { tags: multiselectOptionsToTagIds(selectedReviewTags) }
          : {}),
      },
      documentId: docForm.documentId,
      formId: docForm.formId,
    });

    if (isReviewComplete) {
      await updateStatus(API, docForm.documentId, docForm.formId, "REVIEWED");
    }

    setShowSuccessAlert(true);
    setIsSubmittingReview(false);
    history.goBack();
  };

  const reviewToolbar = (
    <Grid container justify="space-between" spacing={1}>
      <Grid item xs={12}>
        <textarea
          disabled={isReadOnly}
          style={{ width: "100%" }}
          placeholder="Review Notes"
          id="reviewNotesTextArea"
          defaultValue={docForm?.notes ?? ""}
        ></textarea>
      </Grid>
      <Grid item xs={5}>
        <Grid container justify="space-between" spacing={1}>
          <Grid item xs={1}>
            <Box marginTop={0.5} paddingRight={1}>
              <div>Tags</div>
            </Box>
          </Grid>
          <Grid item xs={10}>
            <Box width={"200px"}>
              {isReadOnly ? (
                tagIdsToTags(
                  docForm?.tags ?? [],
                  availableReviewWorkflowTags,
                )?.map((item: any) => (
                  <Badge key={item.tagId} content={item.tagText} />
                ))
              ) : (
                <Multiselect
                  onChange={(tags: any) => {
                    setSelectedReviewTags(tags);
                  }}
                  disabled={isReadOnly}
                  options={reviewTags}
                  value={selectedReviewTags}
                  controlId={"tags"}
                  checkboxes={true}
                />
              )}
            </Box>
          </Grid>
        </Grid>
      </Grid>
      <Grid item xs={1}></Grid>
      <Grid item xs={6}>
        <Grid container alignItems="flex-start" justify="flex-end" spacing={0}>
          <Grid item xs={7}>
            <Checkbox
              disabled={isReadOnly}
              onChange={(e) => {
                setIsReviewComplete(e.target.checked);
              }}
            >
              <Box marginTop={0.5}></Box>
              Review complete
            </Checkbox>
          </Grid>
          <Grid item xs={"auto"}>
            <Button
              disabled={isReadOnly}
              variant={"primary"}
              loading={isSubmittingReview}
              onClick={async () => updateExtractedData()}
            >
              Save
            </Button>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );

  return (
    <Container
      headingVariant="h2"
      title={isReadOnly ? "Viewing Form" : "Reviewing Form"}
      actionGroup={
        <Inline>
          {isReadOnly && (
            <Button
              variant="primary"
              onClick={async () => {
                history.push(
                  `/review/${docForm!.documentId}/${docForm!.formId}`,
                );
                await updateStatus(
                  API,
                  docForm!.documentId,
                  docForm!.formId,
                  "REVIEWING",
                );
              }}
            >
              Review
            </Button>
          )}
          <Button onClick={() => setShowRawDataModal(true)}>
            View Structured Data
          </Button>
        </Inline>
      }
    >
      {showSuccessAlert && (
        <Alert type="success" dismissible={true}>
          Successfully updated review
        </Alert>
      )}
      <Grid container spacing={1}>
        <Grid item xs={12}>
          <Container
            style={{
              marginBottom: "0px",
              boxShadow: "none",
            }}
          >
            <ColumnLayout>
              <Column>
                <Grid container spacing={1}>
                  <Grid item xs={12}>
                    <Container
                      style={{
                        marginBottom: "0px",
                        boxShadow: "none",
                      }}
                      footerContent={reviewToolbar}
                    >
                      <Box style={{ backgroundColor: "red" }}>
                        <Table
                          onSelectionChange={onSelectionChange}
                          getRowId={(row) => row.key}
                          selectedRowIds={
                            selectedFormField.current
                              ? [selectedFormField.current.key]
                              : []
                          }
                          tableTitle="Form Fields"
                          columnDefinitions={formFields}
                          items={formValues}
                          disableGroupBy={true}
                          disableSettings={true}
                          disablePagination={true}
                          disableFilters={true}
                          disableSortBy={true}
                          disableRowSelect={!isReadOnly}
                          multiSelect={false}
                          rowCount={formValues.length}
                          defaultPageSize={formValues.length}
                        />
                      </Box>
                    </Container>
                  </Grid>
                </Grid>
              </Column>
              <Column>
                <PdfViewer
                  url={docForm.url!}
                  drawRef={drawRef}
                  onPageRenderSuccess={onPageRenderSuccess}
                  pageNumber={pageNumber}
                  setPageNumber={setPageNumber}
                />
              </Column>
            </ColumnLayout>
          </Container>
        </Grid>
      </Grid>
      <Modal
        title="Structured Data"
        visible={showRawDataModal}
        onClose={() => setShowRawDataModal(false)}
        width="70%"
      >
        <ColumnLayout>
          <Column>
            <Heading variant="h2">{formSchema.title} Schema</Heading>
            <br />
            <SchemaEditor
              jsonSchema={stringifySchema(docForm.schemaSnapshot)}
            />
          </Column>
          <Column>
            <Heading variant="h2">Extracted Data</Heading>
            <br />
            {docForm.extractedData ? (
              <SchemaEditor
                jsonSchema={stringifyDataAccordingToSchema(
                  docForm.extractedData,
                  docForm.schemaSnapshot,
                )}
              />
            ) : (
              <Alert type="info">Data extraction has not yet completed</Alert>
            )}
          </Column>
        </ColumnLayout>
      </Modal>
    </Container>
  );
};
