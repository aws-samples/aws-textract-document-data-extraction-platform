// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

/**
 * Collection of helper functions to assist with mapping review tag ids to tag
 * objects and to objects consumable by the Multiselect component
 */

export interface ReviewMultiselectTagOption {
  readonly label: string;
  readonly value: string;
}

// return list of review workflow tags matching the passed in list of tag ids
export const tagIdsToTags = (ids: any, tags: any) => {
  return tags && ids
    ? tags.filter((tag: any) => {
        return ids.includes(tag.tagId);
      })
    : [];
};
