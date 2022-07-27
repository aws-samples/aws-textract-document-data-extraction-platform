// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { CreateFormReviewWorkflowTagInput } from "@aws/api/generated/typescript";

/**
 * Sample form review workflow tags from the listings team
 */
export const REVIEW_WORKFLOW_TAGS: CreateFormReviewWorkflowTagInput[] = [
  {
    tagText: "Supervisory Action Taken",
  },
  {
    tagText: "Watchlist Item",
  },
  {
    tagText: "Enforcement Item",
  },
  {
    tagText: "Delay of Disclosure",
  },
  {
    tagText: "Closed Period Trade",
  },
];
