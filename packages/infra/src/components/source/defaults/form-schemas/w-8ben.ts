// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { FormSchemaInput } from "@aws/api/generated/typescript";

/**
 * Default form schema for an Appendix 3X
 */
export const W_8BEN: FormSchemaInput = {
  title: "W-8BEN",
  schema: {
    title: "W-8BEN",
    description:
      "The W-8 form is a legal US Treasury document required by the Internal Revenue Service (IRS) that allows foreign investors to claim concessional tax treaty benefits, including a reduced rate of withholding tax",
    type: "object",
    properties: {
      part1: {
        type: "object",
        order: 1,
        properties: {
          name: {
            title: "Name of individual who is the beneficial owner",
            type: "string",
            order: 1,
            extractionMetadata: {
              formKey: "Name of individual who is the beneficial owner",
              textractQuery:
                "What is the Name of individual who is the beneficial owner?",
            },
          },
          countryOfCitizenship: {
            title: "Country of citizenship",
            type: "string",
            order: 2,
            extractionMetadata: {
              formKey: "Country of citizenship",
              textractQuery: "What is the Country of citizenship?",
            },
          },
          address: {
            title: "Permanent residence address",
            type: "string",
            order: 3,
            extractionMetadata: {
              formKey: "Permanent residence address",
              textractQuery: "What is the Permanent residence address?",
            },
          },
          city: {
            title:
              "City or town, state or province. Include postal code where appropriate.",
            type: "string",
            order: 4,
            extractionMetadata: {
              formKey:
                "City or town, state or province. Include postal code where appropriate.",
              textractQuery:
                "What is the City or town, state or province below the permanent residence address?",
            },
          },
          residenceAddressCountry: {
            title: "Country",
            type: "string",
            order: 5,
            extractionMetadata: {
              formKey: "Country",
              textractQuery: "What is the residence address country?",
            },
          },
          mailingAddress: {
            title: "Mailing address",
            type: "string",
            order: 6,
            extractionMetadata: {
              formKey: "Mailing address (if different from above)",
              textractQuery: "What is the Mailing address?",
            },
          },
          mailingAddressCity: {
            title:
              "City or town, state or province. Include postal code where appropriate.",
            type: "string",
            order: 7,
            extractionMetadata: {
              formKey:
                "City or town, state or province. Include postal code where appropriate.",
              textractQuery:
                "What is the City or town, state or province below the mailing address?",
            },
          },
          mailingAddressCountry: {
            title: "Country",
            type: "string",
            order: 8,
            extractionMetadata: {
              formKey: "Country",
              textractQuery: "What is the Country of the mailing address?",
            },
          },
          ssn: {
            title: "U.S taxpayer identification number(SSN or ITIN)",
            type: "string",
            order: 9,
            extractionMetadata: {
              formKey:
                "U.S taxpayer identification number(SSN or ITIN), if required (see instructions)",
              textractQuery:
                "What is the U.S taxpayer identification number(SSN or ITIN)?",
            },
          },
          foreignTaxID: {
            title: "Foreign tax identifying number (see instructions)",
            type: "string",
            order: 10,
            extractionMetadata: {
              formKey: "Foreign tax identifying number (see instructions)",
              textractQuery: "What is the Foreign tax identifying number?",
            },
          },
          checkFTIN: {
            title: "Check if FTIN not legally required",
            type: "boolean",
            order: 10,
            extractionMetadata: {
              formKey: "Check if FTIN not legally required",
            },
          },
          referenceNumber: {
            title: "Reference number(s) (see instructions)",
            type: "string",
            order: 11,
            extractionMetadata: {
              formKey: "Reference number(s)",
              textractQuery: "What is the Reference number(s)?",
            },
          },
          dateOfBirth: {
            title: "Date of birth (see instructions)",
            type: "string",
            order: 12,
            format: "date",
            extractionMetadata: {
              formKey: "Date of birth",
              textractQuery: "What is the Date of birth?",
            },
          },
        },
        required: [
          "name",
          "countryOfCitizenship",
          "address",
          "city",
          "residenceAddressCountry",
          "ssn",
          "foreignTaxID",
          "referenceNumber",
          "dateOfBirth",
        ],
      },
      part2: {
        type: "object",
        order: 2,
        properties: {
          beneficialOwnerResident: {
            title: "I certify that the beneficial owner is a resident of",
            type: "string",
            order: 1,
            extractionMetadata: {
              formKey: "I certify that the beneficial owner is a resident of",
            },
          },
          specialRatesConditions: {
            title:
              "The beneficial owner is claiming the provisions of Article and paragraph",
            type: "string",
            order: 2,
            extractionMetadata: {
              formKey:
                "The beneficial owner is claiming the provisions of Article and paragraph",
              textractQuery:
                "Which country is the beneficial owner a resident of?",
            },
          },
          specialRatesPercent: {
            title: "of the treaty identified on line 9 above to claim a",
            type: "string",
            order: 3,
            extractionMetadata: {
              formKey: "of the treaty identified on line 9 above to claim a",
              textractQuery:
                "Which provisions of Article and paragraph is the beneficial owner claiming?",
            },
          },
          specialRatesTypeOfIncome: {
            title: "% rate of withholding on (specify type of income)",
            type: "integer",
            order: 4,
            extractionMetadata: {
              formKey: "% rate of withholding on (specify type of income)",
              textractQuery: "What % rate is the beneficial owner withholding?",
            },
          },
          specialRatesAdditionalConditions: {
            title:
              "Explain the additional conditions in the Article and paragraph the beneficial owner meets to be eligible for the rate of withholding",
            type: "string",
            order: 5,
            extractionMetadata: {
              formKey:
                "Explain the additional conditions in the Article and paragraph the beneficial owner meets to be eligible for the rate of withholding",
              textractQuery:
                "What additional conditions in the Article and paragraph is the beneficial owner eligible for?",
            },
          },
        },
      },
    },
    required: ["part1"],
  },
};
