// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import { PaginatedResponse } from "@aws/document-extraction-platform-api-typescript-react-query-hooks";

const DEFAULT_PAGE_SIZE = 100;

interface PaginationParameters {
  pageSize: number;
  nextToken?: string;
}

/**
 * Follow all pages of a paginated api method
 * @param boundApiMethod the method on the api (remember to bind to the API object, eg API.listFoo.bind(API) )
 * @param itemsKey key in the response that contains a page of items
 * @param parameters any non-pagination parameters to pass
 */
export const listAllPages = async <
  O extends PaginatedResponse,
  I extends PaginationParameters,
  K extends string,
>(
  boundApiMethod: (input: I) => Promise<O>,
  itemsKey: K,
  parameters?: Omit<I, keyof PaginationParameters>,
): Promise<K extends keyof O ? O[K] : never> => {
  let nextToken = undefined;
  const items = [];
  do {
    // @ts-ignore
    const response: O = await boundApiMethod({
      ...parameters,
      pageSize: DEFAULT_PAGE_SIZE,
      nextToken,
    });
    nextToken = response.nextToken;
    // @ts-ignore
    items.push(...response[itemsKey]);
  } while (nextToken);

  // @ts-ignore
  return items as O[K];
};
