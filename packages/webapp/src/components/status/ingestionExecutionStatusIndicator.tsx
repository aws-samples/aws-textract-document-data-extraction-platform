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
import { ExecutionStatus } from '@aws/api-typescript';
import { Popover, StatusIndicator } from 'aws-northstar';
import React from 'react';
import { InProgressStatusIndicator } from './inProgressStatusIndicator';

export interface IngestionExecutionStatusIndicatorProps {
  readonly status: ExecutionStatus;
  readonly statusReason?: string;
}

/**
 * Display the status of document ingestion
 */
export const IngestionExecutionStatusIndicator: React.FC<IngestionExecutionStatusIndicatorProps> = ({ status, statusReason }) => {
  switch (status) {
    case 'IN_PROGRESS':
      return <InProgressStatusIndicator label="Classifying" />;
    case 'SUCCEEDED':
      return <StatusIndicator statusType="positive">Classified</StatusIndicator>;
    default:
      const indicator = <StatusIndicator statusType="negative">Failed</StatusIndicator>;
      return (
        <>
          {
            statusReason ? (
              <Popover
                position="bottom"
                size="medium"
                header="Extraction Failed"
                content={statusReason}
              >
                {indicator}
              </Popover>
            ) : indicator
          }
        </>
      );
  }
};
