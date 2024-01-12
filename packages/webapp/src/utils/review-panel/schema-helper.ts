// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import {
  FormJSONSchema,
  FormMetadata,
} from "@aws/document-extraction-platform-api-typescript-react-query-hooks";
import _ from "lodash";

export interface FormValue {
  key: string;
  value: any;
  confidence: number;
  boundingBox: {
    top: number;
    left: number;
    width: number;
    height: number;
  };
  page?: number;
  extractionMethod: string;
}

/**
 * Return a flat dictionary of form fields, given the possibly nested extracted data
 */
export const flattenFormSchema = (documentForm: FormMetadata) => {
  return buildFlattenedFormSchema(
    documentForm.extractedData,
    documentForm.extractedDataMetadata,
    documentForm.schemaSnapshot,
  );
};

export const buildFlattenedFormSchema = (
  formData: any,
  formMetadata: any,
  schema: FormJSONSchema,
  key: string = "",
): FormValue[] => {
  if (schema.typeOf === "object") {
    return getOrderedPropertyKeys(schema.properties!).flatMap((propertyKey) => {
      return buildFlattenedFormSchema(
        formData,
        formMetadata,
        schema.properties![propertyKey],
        `${key}${key ? "." : ""}${propertyKey}`,
      );
    });
  } else if (schema.typeOf === "array") {
    const values = _.get(formData, key) || [];
    return values.flatMap((_value: any, i: number) => {
      return buildFlattenedFormSchema(
        formData,
        formMetadata,
        schema.items!,
        `${key}[${i}]`,
      );
    });
  }

  const metadata = _.get(formMetadata, key) || {
    confidence: 0,
    box: {
      top: 0,
      left: 0,
      width: 0,
      height: 0,
    },
    extractionMethod: "NOT FOUND",
  };

  return [
    {
      key,
      value: _.get(formData, key),
      confidence: metadata.confidence,
      boundingBox: metadata.box,
      page: metadata.page,
      extractionMethod: metadata.extractionMethod,
    },
  ];
};

/**
 * Return the object property keys from the schema in the order defined by their "order" if present
 */
function getOrderedPropertyKeys(properties: { [key: string]: FormJSONSchema }) {
  const keys = Object.keys(properties);
  keys.sort((a, b) => {
    return (
      (properties[a]?.order ?? Infinity) - (properties[b]?.order ?? Infinity)
    );
  });
  return keys;
}

/**
 * Stringify a json schema while respecting the order defined by the "order" property
 */
export const stringifySchema = (schema: FormJSONSchema) =>
  JSON.stringify(
    schema,
    (_key, value) => {
      if (value && typeof value === "object" && !Array.isArray(value)) {
        return Object.fromEntries(
          getOrderedPropertyKeys(value).map((k) => [k, value[k]]),
        );
      }
      return value;
    },
    2,
  );

/**
 * Sort the given data that conforms to the schema based on the order defined by the schema
 */
export const sortDataAccordingToSchema = (
  data: any,
  schema: FormJSONSchema,
): any => {
  if (schema.typeOf === "object") {
    return Object.fromEntries(
      getOrderedPropertyKeys(schema.properties!).map((key) => [
        key,
        sortDataAccordingToSchema(data[key], schema.properties![key]),
      ]),
    );
  } else if (schema.typeOf === "array") {
    return data.map((item: any) =>
      sortDataAccordingToSchema(item, schema.items!),
    );
  }
  // No sorting for primitive types
  return data;
};

/**
 * Stringify extracted data in a more human readable order, based on the schema
 */
export const stringifyDataAccordingToSchema = (
  data: any,
  schema: FormJSONSchema,
) => JSON.stringify(sortDataAccordingToSchema(data, schema), null, 2);
