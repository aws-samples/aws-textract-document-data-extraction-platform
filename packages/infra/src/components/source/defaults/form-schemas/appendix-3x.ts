// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import { FormSchemaInput } from "@aws/api/generated/typescript";

/**
 * Default form schema for an Appendix 3X
 */
export const APPENDIX_3X: FormSchemaInput = {
  title: "Appendix 3X",
  schema: {
    title: "Company Announcements 3X",
    description: "Initial Director's Interest Notices",
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
          appointmentDate: {
            title: "Date of Appointment",
            typeOf: "string",
            formatType: "date",
            order: 4,
            extractionMetadata: {
              formKey: "Date of appointment",
              tablePosition: 2,
              rowPosition: 2,
              columnPosition: 2,
            },
          },
          securityNumberClass: {
            title: "Number & Class of Securities",
            typeOf: "string",
            order: 5,
            extractionMetadata: {
              formKey: "Number & class of securities",
              tablePosition: 3,
              rowPosition: 1,
              columnPosition: 1,
            },
          },
        },
        required: ["entityName", "abn", "directorName", "appointmentDate"],
      },
      part2: {
        typeOf: "object",
        order: 2,
        properties: {
          holderInterest: {
            title: "Name of Holder & Nature of Interest",
            typeOf: "string",
            order: 1,
            extractionMetadata: {
              formKey: "Name of holder & nature of interest",
              tablePosition: 4,
              rowPosition: 1,
              columnPosition: 1,
              textractQuery: "What is the name of holder & nature of interest?",
            },
          },
          holderSecurity: {
            title: "Number & Class of Securities",
            typeOf: "string",
            order: 2,
            extractionMetadata: {
              formKey: "Number & class of Securities",
              tablePosition: 4,
              rowPosition: 1,
              columnPosition: 2,
              textractQuery: "What is the number & class of securities?",
            },
          },
        },
      },
      part3: {
        typeOf: "object",
        order: 3,
        properties: {
          contactDetails: {
            title: "Detail of Contract",
            typeOf: "string",
            order: 1,
            extractionMetadata: {
              formKey: "Detail of contract",
              tablePosition: 5,
              rowPosition: 1,
              columnPosition: 2,
            },
          },
          natureInterest: {
            title: "Nature of Interest",
            typeOf: "string",
            order: 2,
            extractionMetadata: {
              formKey: "Nature of interest",
              textractQuery: "What is the nature of interest?",
              tablePosition: 5,
              rowPosition: 2,
              columnPosition: 2,
            },
          },
          registeredHolder: {
            title: "Name of Registered Holder",
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
            title: "No. and Class of Securities to Which Interest Relates",
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
