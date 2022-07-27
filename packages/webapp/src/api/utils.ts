/**********************************************************************************************************************
 *  Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                           *
 *                                                                                                                    *
 *  Licensed under the Amazon Software License (the "License"). You may not use this file except in compliance        *
 *  with the License. A copy of the License is located at                                                             *
 *                                                                                                                    *
 *     http://aws.amazon.com/asl/                                                                                     *
 *                                                                                                                    *
 *  or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES *
 *  OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions    *
 *  and limitations under the License.                                                                                *
 **********************************************************************************************************************/
import { PaginatedResponse } from '@aws/api-typescript';

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
export const listAllPages = async <O extends PaginatedResponse, I extends PaginationParameters, K extends string>(
  boundApiMethod: (input: I) => Promise<O>,
  itemsKey: K,
  parameters?: Omit<I, keyof PaginationParameters>,
): Promise<K extends keyof O ? O[K] : never> => {
  let nextToken = undefined;
  const items = [];
  do {
    // @ts-ignore
    const response: O = await boundApiMethod({ ...parameters, pageSize: DEFAULT_PAGE_SIZE, nextToken });
    nextToken = response.nextToken;
    // @ts-ignore
    items.push(...response[itemsKey]);
  } while (nextToken);

  // @ts-ignore
  return items as O[K];
};
