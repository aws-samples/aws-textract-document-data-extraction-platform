/* tslint:disable */
/* eslint-disable */
/**
 * AWS Docs API
 * API for AWS Docs
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
import {
    DocumentMetadata,
    DocumentMetadataFromJSON,
    DocumentMetadataFromJSONTyped,
    DocumentMetadataToJSON,
} from './DocumentMetadata';
import {
    PaginatedResponse,
    PaginatedResponseFromJSON,
    PaginatedResponseFromJSONTyped,
    PaginatedResponseToJSON,
} from './PaginatedResponse';

/**
 * A list of documents
 * @export
 * @interface ListDocumentsResponse
 */
export interface ListDocumentsResponse {
    /**
     * 
     * @type {Array<DocumentMetadata>}
     * @memberof ListDocumentsResponse
     */
    documents: Array<DocumentMetadata>;
    /**
     * 
     * @type {string}
     * @memberof ListDocumentsResponse
     */
    nextToken?: string;
}


export function ListDocumentsResponseFromJSON(json: any): ListDocumentsResponse {
    return ListDocumentsResponseFromJSONTyped(json, false);
}

export function ListDocumentsResponseFromJSONTyped(json: any, ignoreDiscriminator: boolean): ListDocumentsResponse {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'documents': ((json['documents'] as Array<any>).map(DocumentMetadataFromJSON)),
        'nextToken': !exists(json, 'nextToken') ? undefined : json['nextToken'],
    };
}

export function ListDocumentsResponseToJSON(value?: ListDocumentsResponse | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'documents': ((value.documents as Array<any>).map(DocumentMetadataToJSON)),
        'nextToken': value.nextToken,
    };
}

