// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { FormSchemaInput } from "@aws/api/generated/typescript";

/**
 * Default form schema for an Appendix 3Z
 */
export const APPENDIX_3Z: FormSchemaInput = {
  title: "Appendix 3Z",
  schema: {
    title: "Company Announcements 3Z",
    description: "Final Director's Interest Notices",
    typeOf: "object",
    properties: {
      part1: {
        typeOf: "object",
        order: 1,
        properties: {
          entityName: {
            title: "Name of Entity",
            typeOf: "string",
            order: 1,
            extractionMetadata: {
              formKey: "Name of entity",
              tablePosition: 1,
              rowPosition: 1,
              columnPosition: 2,
              textractQuery: "What is the Name of entity?",
            },
          },
          abn: {
            title: "ABN",
            typeOf: "string",
            order: 2,
            extractionMetadata: {
              formKey: "ABN",
              tablePosition: 1,
              rowPosition: 2,
              columnPosition: 2,
              textractQuery: "What is the ABN or ARBN?",
            },
          },
          directorName: {
            title: "Name of Director",
            typeOf: "string",
            order: 3,
            extractionMetadata: {
              formKey: "Name of director",
              tablePosition: 2,
              rowPosition: 1,
              columnPosition: 2,
              textractQuery: "What is the Name of director?",
            },
          },
          lastNoticeDate: {
            title: "Date of Last Notice",
            typeOf: "string",
            formatType: "date",
            order: 4,
            extractionMetadata: {
              formKey: "Date of last notice",
              tablePosition: 2,
              rowPosition: 2,
              columnPosition: 2,
              textractQuery: "What is the date of last notice?",
            },
          },
          ceaseDirectorDate: {
            title: "Date that Director Ceased to be Director",
            typeOf: "string",
            formatType: "date",
            order: 5,
            extractionMetadata: {
              formKey: "Date that director ceased to be director",
              tablePosition: 2,
              rowPosition: 3,
              columnPosition: 2,
              textractQuery:
                "What is the date that director ceased to be director?",
            },
          },
          relevantInterestSecurities: {
            title: "Number & class of securities",
            typeOf: "string",
            order: 6,
            extractionMetadata: {
              formKey: "Number & class of securities",
              tablePosition: 3,
              rowPosition: 1,
              columnPosition: 1,
              textractQuery: "What is the Number & class of securities?",
            },
          },
        },
        required: ["entityName", "abn", "directorName", "lastNoticeDate"],
      },
      part2: {
        typeOf: "object",
        order: 2,
        properties: {
          holderNameInterest: {
            title: "Name of holder & nature of interest",
            typeOf: "string",
            order: 1,
            extractionMetadata: {
              formKey: "Name of holder & nature of interest",
              tablePosition: 4,
              rowPosition: 1,
              columnPosition: 1,
              textractQuery: "What is the Name of holder & nature of interest?",
            },
          },
          securitiesClass: {
            title: "Number & class of securities",
            typeOf: "string",
            order: 2,
            extractionMetadata: {
              formKey: "Number & class of securities",
              tablePosition: 4,
              rowPosition: 1,
              columnPosition: 2,
              // NB: queries can't be duplicated, but we can add more ?s to trick textract into allowing multiple.
              // Relative order of fields then narrows down which query answer to pick at extraction time.
              textractQuery: "What is the Number & class of securities??",
            },
          },
        },
      },
      part3: {
        typeOf: "object",
        order: 3,
        properties: {
          contractDetails: {
            title: "Detail of contract",
            typeOf: "string",
            order: 1,
            extractionMetadata: {
              formKey: "Detail of contract",
              tablePosition: 5,
              rowPosition: 1,
              columnPosition: 2,
              textractQuery: "What is the Detail of contract?",
            },
          },
          natureInterest: {
            title: "Nature of interest",
            typeOf: "string",
            order: 2,
            extractionMetadata: {
              formKey: "Nature of interest",
              tablePosition: 5,
              rowPosition: 2,
              columnPosition: 2,
              textractQuery: "What is the Nature of interest?",
            },
          },
          registeredHolder: {
            title: "Name of registered holder",
            typeOf: "string",
            order: 3,
            extractionMetadata: {
              formKey: "Name of registered holder (if issued securities)",
              tablePosition: 5,
              rowPosition: 3,
              columnPosition: 2,
            },
          },
          existingSecurities: {
            title: "No. and class of securities to which interest relates",
            typeOf: "string",
            order: 4,
            extractionMetadata: {
              formKey: "No. and class of securities to which interest relates",
              tablePosition: 5,
              rowPosition: 4,
              columnPosition: 2,
            },
          },
        },
      },
    },
    required: ["part1"],
  },
};
