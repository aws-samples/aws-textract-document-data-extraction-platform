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
/**
 * Metadata to assist with the extraction of this form field from a document
 * @export
 * @interface FormFieldExtractionMetadata
 */
export interface FormFieldExtractionMetadata {
    /**
     * The literal text uses as the key for this field in a form, eg 'Name of Entity'. Capitalisation should be the same as appears in the form.
     * @type {string}
     * @memberof FormFieldExtractionMetadata
     */
    formKey?: string;
    /**
     * The 1-indexed table number in which this field appears.
     * @type {number}
     * @memberof FormFieldExtractionMetadata
     */
    tablePosition?: number;
    /**
     * The 1-indexed row number within the table in which this field appears
     * @type {number}
     * @memberof FormFieldExtractionMetadata
     */
    rowPosition?: number;
    /**
     * The 1-indexed column number within the table in which this field appears.
     * @type {number}
     * @memberof FormFieldExtractionMetadata
     */
    columnPosition?: number;
    /**
     * When specified, try to extract the field using this textract query before falling back to other means
     * @type {string}
     * @memberof FormFieldExtractionMetadata
     */
    textractQuery?: string;
}


export function FormFieldExtractionMetadataFromJSON(json: any): FormFieldExtractionMetadata {
    return FormFieldExtractionMetadataFromJSONTyped(json, false);
}

export function FormFieldExtractionMetadataFromJSONTyped(json: any, ignoreDiscriminator: boolean): FormFieldExtractionMetadata {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'formKey': !exists(json, 'formKey') ? undefined : json['formKey'],
        'tablePosition': !exists(json, 'tablePosition') ? undefined : json['tablePosition'],
        'rowPosition': !exists(json, 'rowPosition') ? undefined : json['rowPosition'],
        'columnPosition': !exists(json, 'columnPosition') ? undefined : json['columnPosition'],
        'textractQuery': !exists(json, 'textractQuery') ? undefined : json['textractQuery'],
    };
}

export function FormFieldExtractionMetadataToJSON(value?: FormFieldExtractionMetadata | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'formKey': value.formKey,
        'tablePosition': value.tablePosition,
        'rowPosition': value.rowPosition,
        'columnPosition': value.columnPosition,
        'textractQuery': value.textractQuery,
    };
}
