// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { FormSchemaInput } from "@aws/api/generated/typescript";

/**
 * Default form schema for an Appendix 3Y
 */
export const APPENDIX_3Y: FormSchemaInput = {
  title: "Appendix 3Y",
  schema: {
    title: "Company Announcements 3Y",
    description: "Change of Director's Interest Notices",
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
            },
          },
          directorName: {
            title: "Name of Director",
            typeOf: "string",
            order: 3,
            extractionMetadata: {
              formKey: "Name of Director",
              tablePosition: 2,
              rowPosition: 1,
              columnPosition: 2,
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
            },
          },
          directNoticeFlag: {
            title: "Direct or indirect interest",
            typeOf: "string",
            order: 5,
            extractionMetadata: {
              formKey: "Direct or indirect interest",
              tablePosition: 3,
              rowPosition: 1,
              columnPosition: 2,
              textractQuery: "What is the direct or indirect interest?",
            },
          },
          dateChange: {
            title: "Date of Change",
            typeOf: "string",
            formatType: "date",
            order: 6,
            extractionMetadata: {
              formKey: "Date of change",
              tablePosition: 3,
              rowPosition: 3,
              columnPosition: 2,
            },
          },
          securitiesPrior: {
            title: "No. of securities held prior to change",
            typeOf: "string",
            order: 7,
            extractionMetadata: {
              formKey: "No. of securities held prior to change",
              tablePosition: 3,
              rowPosition: 4,
              columnPosition: 2,
            },
          },
          class: {
            title: "Class",
            typeOf: "string",
            order: 8,
            extractionMetadata: {
              formKey: "Class",
              tablePosition: 3,
              rowPosition: 5,
              columnPosition: 2,
            },
          },
          securitiesAcquired: {
            title: "Number acquired",
            typeOf: "string",
            order: 9,
            extractionMetadata: {
              formKey: "Number acquired",
              tablePosition: 3,
              rowPosition: 6,
              columnPosition: 2,
            },
          },
          securitiesDisposed: {
            title: "Number disposed",
            typeOf: "string",
            order: 10,
            extractionMetadata: {
              formKey: "Number disposed",
              tablePosition: 3,
              rowPosition: 7,
              columnPosition: 2,
            },
          },
          securitiesValue: {
            title: "Value/Consideration",
            typeOf: "string",
            order: 11,
            extractionMetadata: {
              formKey: "Value/Consideration",
              tablePosition: 3,
              rowPosition: 8,
              columnPosition: 2,
            },
          },
          securitiesHeldAfter: {
            title: "No. of securities held after change",
            typeOf: "string",
            order: 12,
            extractionMetadata: {
              formKey: "No. of securities held after change",
              tablePosition: 3,
              rowPosition: 9,
              columnPosition: 2,
            },
          },
          natureOfChange: {
            title: "Nature of change",
            typeOf: "string",
            order: 13,
            extractionMetadata: {
              formKey: "Nature of change",
              tablePosition: 3,
              rowPosition: 10,
              columnPosition: 2,
              textractQuery: "What is to the right of the Nature of change?",
            },
          },
        },
        required: [
          "entityName",
          "abn",
          "directorName",
          "lastNoticeDate",
          "directNoticeFlag",
          "dateChange",
          "securitiesPrior",
          "class",
          "securitiesAcquired",
          "securitiesDisposed",
          "securitiesValue",
          "securitiesHeldAfter",
          "natureOfChange",
        ],
      },
      part2: {
        typeOf: "object",
        order: 2,
        properties: {
          contractDetail: {
            title: "Detail of contract",
            typeOf: "string",
            order: 1,
            extractionMetadata: {
              formKey: "Detail of contract",
              tablePosition: 4,
              rowPosition: 1,
              columnPosition: 2,
            },
          },
          interestNature: {
            title: "Nature of interest",
            typeOf: "string",
            order: 2,
            extractionMetadata: {
              formKey: "Nature of interest",
              tablePosition: 4,
              rowPosition: 2,
              columnPosition: 2,
            },
          },
          registeredHolder: {
            title: "Name of registered holder",
            typeOf: "string",
            order: 3,
            extractionMetadata: {
              formKey: "Name of registered holder (if issued securities)",
              tablePosition: 4,
              rowPosition: 3,
              columnPosition: 2,
            },
          },
          changeDate2: {
            title: "date Change 2",
            typeOf: "string",
            formatType: "date",
            order: 4,
            extractionMetadata: {
              formKey: "Date of change",
              tablePosition: 4,
              rowPosition: 4,
              columnPosition: 2,
            },
          },
          securitiesInterestPrior: {
            title:
              "No. and class of securities to which interest related prior to change",
            typeOf: "string",
            order: 5,
            extractionMetadata: {
              formKey:
                "No. and class of securities to which interest related prior to change Note: Details are only required for a contract in relation to which the interest has changed",
              tablePosition: 4,
              rowPosition: 5,
              columnPosition: 1,
            },
          },
          interestAcquired: {
            title: "Interest acquired",
            typeOf: "string",
            order: 6,
            extractionMetadata: {
              formKey: "Interest acquired",
              tablePosition: 4,
              rowPosition: 6,
              columnPosition: 2,
            },
          },
          interestDisposed: {
            title: "Interest disposed",
            typeOf: "string",
            order: 7,
            extractionMetadata: {
              formKey: "Interest disposed",
              tablePosition: 4,
              rowPosition: 7,
              columnPosition: 2,
            },
          },
          interestValue: {
            title: "Value/Consideration",
            typeOf: "string",
            order: 8,
            extractionMetadata: {
              formKey: "Value/Consideration",
              tablePosition: 4,
              rowPosition: 8,
              columnPosition: 2,
            },
          },
          securitiesInterestAfter: {
            title: "Interest after change",
            typeOf: "string",
            order: 9,
            extractionMetadata: {
              formKey: "Interest after change",
              tablePosition: 4,
              rowPosition: 9,
              columnPosition: 2,
            },
          },
        },
      },
    },
    required: ["part1"],
  },
};
