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
    FormJSONSchema,
    FormJSONSchemaFromJSON,
    FormJSONSchemaFromJSONTyped,
    FormJSONSchemaToJSON,
} from './FormJSONSchema';

/**
 * A schema defining the structured data expected for a form (without an id)
 * @export
 * @interface FormSchemaInput
 */
export interface FormSchemaInput {
    /**
     * The title of the form, as it appears in the form, eg 'Appendix 3x'
     * @type {string}
     * @memberof FormSchemaInput
     */
    title: string;
    /**
     * A description of the form and schema
     * @type {string}
     * @memberof FormSchemaInput
     */
    description?: string;
    /**
     * 
     * @type {FormJSONSchema}
     * @memberof FormSchemaInput
     */
    schema: FormJSONSchema;
}


export function FormSchemaInputFromJSON(json: any): FormSchemaInput {
    return FormSchemaInputFromJSONTyped(json, false);
}

export function FormSchemaInputFromJSONTyped(json: any, ignoreDiscriminator: boolean): FormSchemaInput {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'title': json['title'],
        'description': !exists(json, 'description') ? undefined : json['description'],
        'schema': FormJSONSchemaFromJSON(json['schema']),
    };
}

export function FormSchemaInputToJSON(value?: FormSchemaInput | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'title': value.title,
        'description': value.description,
        'schema': FormJSONSchemaToJSON(value.schema),
    };
}

