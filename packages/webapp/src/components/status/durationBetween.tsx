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
import { StatusTransition } from '@aws/api-typescript';
import humanizeDuration from 'humanize-duration';
import React, { useMemo } from 'react';

export interface DurationBetweenProps {
  fromStatuses: string[];
  toStatuses: string[];
  statusTransitionLog: StatusTransition[];
}

/**
 * Displays a human readable duration between the transition between the given statuses
 */
export const DurationBetween: React.FC<DurationBetweenProps> = ({ fromStatuses, toStatuses, statusTransitionLog }) => {
  const toStatusesSet = useMemo(() => new Set(toStatuses), [toStatuses]);
  const fromStatusesSet = useMemo(() => new Set(fromStatuses), [fromStatuses]);

  // Find the first occurrence of the "from" status
  const fromTimestamp = useMemo(() => statusTransitionLog.find(
    ({ status }) => fromStatusesSet.has(status),
  )?.timestamp, [fromStatusesSet, statusTransitionLog]);

  // Find the last occurrence of the "to" status
  const toTimestamp = useMemo(() => statusTransitionLog.reverse().find(
    ({ status }) => toStatusesSet.has(status),
  )?.timestamp, [toStatusesSet, statusTransitionLog]);

  return (
    <>
      {
        fromTimestamp && toTimestamp ? (
          humanizeDuration(new Date(toTimestamp).getTime() - new Date(fromTimestamp).getTime(), { largest: 2, round: true })
        ) : 'N/A'
      }
    </>
  );
};
