// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { FormSchemaInput } from "@aws/api/generated/typescript";

/**
 * Default form schema for an Appendix 3X
 */
export const MARGIN_LENDING: FormSchemaInput = {
  title: "MARGIN LENDING",
  schema: {
    title: "MARGIN LENDING",
    description: "Refinance request form for margin lending",
    type: "object",
    properties: {
      part1: {
        type: "object",
        order: 1,
        properties: {
          borrowerName: {
            title: "Borrower name",
            type: "string",
            order: 1,
            extractionMetadata: {
              formKey: "BORROWER(S) NAME(S)",
              textractQuery: "What is the borrower name?",
            },
          },
          commsecLoanAccountNumber: {
            title: "Commsec margin loan account number",
            type: "string",
            order: 2,
            extractionMetadata: {
              formKey: "COMMSEC MARGIN LOAN ACCOUNT NUMBER",
              textractQuery: "What is the COMMSEC MARGIN LOAN ACCOUNT NUMBER?",
            },
          },
          address: {
            title: "borrowers residential address",
            type: "string",
            order: 3,
            extractionMetadata: {
              formKey: "BORROWERS RESIDENTIAL ADDRESS",
              textractQuery: "What is the BORROWERS RESIDENTIAL ADDRESS?",
            },
          },
          state: {
            title: "state",
            type: "string",
            order: 4,
            extractionMetadata: {
              formKey: "STATE",
              textractQuery: "What is the state?",
            },
          },
          postcode: {
            title: "postcode",
            type: "integer",
            order: 5,
            extractionMetadata: {
              formKey: "POSTCODE",
              textractQuery: "What is the postcode?",
            },
          },
          phone: {
            title: "phone",
            type: "string",
            order: 6,
            extractionMetadata: {
              formKey: "PHONE",
              textractQuery: "What is the phone?",
            },
          },
          email: {
            title: "email",
            type: "string",
            order: 7,
            extractionMetadata: {
              formKey: "EMAIL",
              textractQuery: "What is the email?",
            },
          },
        },
        required: [
          "borrowerName",
          "commsecLoanAccountNumber",
          "address",
          "state",
          "postcode",
          "phone",
          "email",
        ],
      },
      part2: {
        type: "object",
        order: 2,
        properties: {
          marginLoanProvider: {
            title: "Margin loan provider",
            type: "string",
            order: 1,
            extractionMetadata: {
              formKey: "MARGIN LOAN PROVIDER",
              textractQuery: "Who is the margin loan provider?",
            },
          },
          marginLoanName: {
            title: "Margin Loan Account Name",
            type: "string",
            order: 2,
            extractionMetadata: {
              formKey: "NAME IN WHICH MARGIN LOAN ACCOUNT HELD",
              textractQuery:
                "What is the name in which the margin loan account was held?",
            },
          },
          loanAccountNumber: {
            title: "Margin Loan Account Number",
            type: "string",
            order: 3,
            extractionMetadata: {
              formKey: "MARGIN LOAN ACCOUNT NUMBER",
              textractQuery: "What is the margin loan account number?",
            },
          },
          hin: {
            title: "HIN",
            type: "string",
            order: 4,
            extractionMetadata: {
              formKey: "HIN",
              textractQuery: "What is the HIN?",
            },
          },
          checkTransferAllChess: {
            title: "Please transfer ALL of my CHESS shareholdings",
            type: "boolean",
            _default: false,
            order: 5,
            extractionMetadata: {
              formKey:
                "Please transfer ALL of my/our CHESS shareholdings/Managed Funds and Holder Identification Number (HIN)",
              textractQuery:
                "Is the checkbox ticked for please transfer all of my/our CHESS shareholdings?",
            },
          },
          checkTransferChess: {
            title:
              "Please transfer the CHESS shareholdings or Managed funds listed",
            type: "boolean",
            _default: false,
            order: 6,
            extractionMetadata: {
              formKey:
                "Please transfer the CHESS shareholdings or Managed funds listed",
              textractQuery:
                "Is the checkbox ticked for please transfer the CHESS shareholdings or Managed funds listed?",
            },
          },
          awsCodeAPIR: {
            title: "ASX CODE / APIR",
            type: "string",
            order: 7,
            extractionMetadata: {
              formKey: "ASX CODE / APIR",
              textractQuery: "what is the ASX CODE / APIR?",
            },
          },
          securityNameManagedFund: {
            title: "SECURITY NAME / MANAGED FUND",
            type: "string",
            order: 8,
            extractionMetadata: {
              formKey: "SECURITY NAME / MANAGED FUND",
              textractQuery: "What is the SECURITY NAME / MANAGED FUND?",
            },
          },
          noOfUnits: {
            title: "No. Units",
            type: "integer",
            order: 9,
            extractionMetadata: {
              formKey: "NO. UNITS",
              textractQuery: "What is the No. Units?",
            },
          },
          isLoanStatementAttached: {
            title: "isLoanStatementAttached",
            type: "boolean",
            order: 10,
            _default: false,
            extractionMetadata: {
              formKey:
                "I / we have attached my/our most recent Margin Loan statement",
              textractQuery:
                "Is the 'I / we have attached my/our most recent Margin Loan statement' checkbox ticked?",
            },
          },
          balanceToBeTransferred: {
            title: "Balance",
            type: "number",
            order: 11,
            extractionMetadata: {
              formKey: "Balance of the margin loan to be transferred",
              textractQuery:
                "What is the Balance of the margin loan to be transferred?",
            },
          },
          isLoanAmountWholeLoanBalance: {
            title: "isLoanAmountWholeLoanBalance",
            type: "boolean",
            _default: false,
            order: 12,
            extractionMetadata: {
              formKey:
                "Please tick if the loan amount to be transferred is the whole loan balance",
              textractQuery:
                "Is the 'Please tick if the loan amount to be transferred is the whole loan balance' checkbox ticked?",
            },
          },
        },
        required: [
          "marginLoanProvider",
          "marginLoanName",
          "loanAccountNumber",
          "hin",
          "awsCodeAPIR",
          "securityNameManagedFund",
          "noOfUnits",
          "balanceToBeTransferred",
        ],
      },
    },
    required: ["part1", "part2"],
  },
};
