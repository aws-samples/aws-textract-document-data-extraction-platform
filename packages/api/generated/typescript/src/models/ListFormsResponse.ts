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
    FormMetadata,
    FormMetadataFromJSON,
    FormMetadataFromJSONTyped,
    FormMetadataToJSON,
} from './FormMetadata';
import {
    PaginatedResponse,
    PaginatedResponseFromJSON,
    PaginatedResponseFromJSONTyped,
    PaginatedResponseToJSON,
} from './PaginatedResponse';

/**
 * A list of forms
 * @export
 * @interface ListFormsResponse
 */
export interface ListFormsResponse {
    /**
     * 
     * @type {Array<FormMetadata>}
     * @memberof ListFormsResponse
     */
    forms: Array<FormMetadata>;
    /**
     * 
     * @type {string}
     * @memberof ListFormsResponse
     */
    nextToken?: string;
}


export function ListFormsResponseFromJSON(json: any): ListFormsResponse {
    return ListFormsResponseFromJSONTyped(json, false);
}

export function ListFormsResponseFromJSONTyped(json: any, ignoreDiscriminator: boolean): ListFormsResponse {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'forms': ((json['forms'] as Array<any>).map(FormMetadataFromJSON)),
        'nextToken': !exists(json, 'nextToken') ? undefined : json['nextToken'],
    };
}

export function ListFormsResponseToJSON(value?: ListFormsResponse | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'forms': ((value.forms as Array<any>).map(FormMetadataToJSON)),
        'nextToken': value.nextToken,
    };
}

