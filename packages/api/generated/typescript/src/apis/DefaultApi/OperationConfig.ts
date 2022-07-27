// Import models
import {
    AggregateMetrics,
    AggregateMetricsFromJSON,
    AggregateMetricsToJSON,
    ApiError,
    ApiErrorFromJSON,
    ApiErrorToJSON,
    CreateFormReviewWorkflowTagInput,
    CreateFormReviewWorkflowTagInputFromJSON,
    CreateFormReviewWorkflowTagInputToJSON,
    DocumentMetadata,
    DocumentMetadataFromJSON,
    DocumentMetadataToJSON,
    FormMetadata,
    FormMetadataFromJSON,
    FormMetadataToJSON,
    FormReviewWorkflowTag,
    FormReviewWorkflowTagFromJSON,
    FormReviewWorkflowTagToJSON,
    FormSchema,
    FormSchemaFromJSON,
    FormSchemaToJSON,
    FormSchemaInput,
    FormSchemaInputFromJSON,
    FormSchemaInputToJSON,
    GetDocumentUploadUrlResponse,
    GetDocumentUploadUrlResponseFromJSON,
    GetDocumentUploadUrlResponseToJSON,
    ListDocumentsResponse,
    ListDocumentsResponseFromJSON,
    ListDocumentsResponseToJSON,
    ListFormReviewWorkflowTagsResponse,
    ListFormReviewWorkflowTagsResponseFromJSON,
    ListFormReviewWorkflowTagsResponseToJSON,
    ListFormSchemasResponse,
    ListFormSchemasResponseFromJSON,
    ListFormSchemasResponseToJSON,
    ListFormsResponse,
    ListFormsResponseFromJSON,
    ListFormsResponseToJSON,
    SubmitSourceDocumentInput,
    SubmitSourceDocumentInputFromJSON,
    SubmitSourceDocumentInputToJSON,
    UpdateFormInput,
    UpdateFormInputFromJSON,
    UpdateFormInputToJSON,
    UpdateStatusInput,
    UpdateStatusInputFromJSON,
    UpdateStatusInputToJSON,
} from '../../models';
// Import request parameter interfaces
import {
    CreateFormReviewWorkflowTagRequest,
    CreateFormSchemaRequest,
    DeleteFormSchemaRequest,
    GetDocumentRequest,
    GetDocumentFormRequest,
    GetDocumentUploadUrlRequest,
    GetFormSchemaRequest,
    GetMetricsRequest,
    ListDocumentFormsRequest,
    ListDocumentsRequest,
    ListFormReviewWorkflowTagsRequest,
    ListFormSchemasRequest,
    ListFormsRequest,
    SubmitSourceDocumentRequest,
    UpdateFormReviewRequest,
    UpdateFormSchemaRequest,
    UpdateStatusRequest,
} from '..';

// Generic type for object keyed by operation names
export interface OperationConfig<T> {
    createFormReviewWorkflowTag: T;
    createFormSchema: T;
    deleteFormSchema: T;
    getDocument: T;
    getDocumentForm: T;
    getDocumentUploadUrl: T;
    getFormSchema: T;
    getMetrics: T;
    listDocumentForms: T;
    listDocuments: T;
    listFormReviewWorkflowTags: T;
    listFormSchemas: T;
    listForms: T;
    submitSourceDocument: T;
    updateFormReview: T;
    updateFormSchema: T;
    updateStatus: T;
}

// Look up path and http method for a given operation name
export const OperationLookup = {
    createFormReviewWorkflowTag: {
        path: '/tags',
        method: 'POST',
    },
    createFormSchema: {
        path: '/schemas',
        method: 'POST',
    },
    deleteFormSchema: {
        path: '/schemas/{schemaId}',
        method: 'DELETE',
    },
    getDocument: {
        path: '/documents/{documentId}',
        method: 'GET',
    },
    getDocumentForm: {
        path: '/documents/{documentId}/forms/{formId}',
        method: 'GET',
    },
    getDocumentUploadUrl: {
        path: '/documents/upload-url',
        method: 'GET',
    },
    getFormSchema: {
        path: '/schemas/{schemaId}',
        method: 'GET',
    },
    getMetrics: {
        path: '/metrics',
        method: 'GET',
    },
    listDocumentForms: {
        path: '/documents/{documentId}/forms',
        method: 'GET',
    },
    listDocuments: {
        path: '/documents',
        method: 'GET',
    },
    listFormReviewWorkflowTags: {
        path: '/tags',
        method: 'GET',
    },
    listFormSchemas: {
        path: '/schemas',
        method: 'GET',
    },
    listForms: {
        path: '/forms',
        method: 'GET',
    },
    submitSourceDocument: {
        path: '/sources/document',
        method: 'POST',
    },
    updateFormReview: {
        path: '/documents/{documentId}/forms/{formId}/review',
        method: 'PUT',
    },
    updateFormSchema: {
        path: '/schemas/{schemaId}',
        method: 'PUT',
    },
    updateStatus: {
        path: '/documents/{documentId}/forms/{formId}/status',
        method: 'PUT',
    },
};

// Standard apigateway request parameters (query parameters or path parameters, multi or single value)
type ApiGatewayRequestParameters = { [key: string]: string | string[] | undefined };

/**
 * URI decode for a string or array of strings
 */
const uriDecode = (value: string | string[]): string | string[] =>
    typeof value === 'string' ? decodeURIComponent(value) : value.map((v) => decodeURIComponent(v));

/**
 * URI decodes apigateway request parameters (query or path parameters)
 */
const decodeRequestParameters = (parameters: ApiGatewayRequestParameters): ApiGatewayRequestParameters => {
    const decodedParameters = {};
    Object.keys(parameters || {}).forEach((key) => {
        decodedParameters[key] = parameters[key] ? uriDecode(parameters[key]) : parameters[key];
    });
    return decodedParameters;
};

/**
 * Parse the body if the content type is json, otherwise leave as a raw string
 */
const parseBody = (body: string, contentTypes: string[]): any => contentTypes.filter((contentType) => contentType !== 'application/json').length === 0 ? JSON.parse(body || '{}') : body;

// Api gateway lambda handler type
type ApiGatewayLambdaHandler = (event: any, context: any) => Promise<any>;

// Type of the response to be returned by an operation lambda handler
export interface OperationResponse<T, ApiError> {
    statusCode: number;
    headers?: { [key: string]: string };
    body?: T | ApiError;
}

// Input for a lambda handler for an operation
export type LambdaRequestParameters<RequestParameters, RequestArrayParameters, RequestBody> = {
    requestParameters: RequestParameters,
    requestArrayParameters: RequestArrayParameters,
    body: RequestBody,
};

// Type for a lambda handler function to be wrapped
export type LambdaHandlerFunction<RequestParameters, RequestArrayParameters, RequestBody, RequestOutput, ApiError> = (
    input: LambdaRequestParameters<RequestParameters, RequestArrayParameters, RequestBody>,
    event: any,
    context: any,
) => Promise<OperationResponse<RequestOutput, ApiError>>;

// Type alias for the request
type CreateFormReviewWorkflowTagRequestInput = CreateFormReviewWorkflowTagRequest;

/**
 * Single-value path/query parameters for CreateFormReviewWorkflowTag
 */
export interface CreateFormReviewWorkflowTagRequestParameters {
}

/**
 * Multi-value query parameters for CreateFormReviewWorkflowTag
 */
export interface CreateFormReviewWorkflowTagRequestArrayParameters {
}

/**
 * Request body parameter for CreateFormReviewWorkflowTag
 */
export type CreateFormReviewWorkflowTagRequestBody = CreateFormReviewWorkflowTagInput;

// Type that the handler function provided to the wrapper must conform to
type CreateFormReviewWorkflowTagHandlerFunction<ApiError> = LambdaHandlerFunction<CreateFormReviewWorkflowTagRequestParameters, CreateFormReviewWorkflowTagRequestArrayParameters, CreateFormReviewWorkflowTagRequestBody, FormReviewWorkflowTag, ApiError>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of createFormReviewWorkflowTag
 */
export const createFormReviewWorkflowTagHandler = <ApiError>(handler: CreateFormReviewWorkflowTagHandlerFunction<ApiError>): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as CreateFormReviewWorkflowTagRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as CreateFormReviewWorkflowTagRequestArrayParameters;

    const body = parseBody(event.body, ['application/json',]) as CreateFormReviewWorkflowTagRequestBody;

    const response = await handler({
        requestParameters,
        requestArrayParameters,
        body,
    }, event, context);

    return {
        ...response,
        body: response.body ? JSON.stringify(response.body) : '',
    };
};
// Type alias for the request
type CreateFormSchemaRequestInput = CreateFormSchemaRequest;

/**
 * Single-value path/query parameters for CreateFormSchema
 */
export interface CreateFormSchemaRequestParameters {
}

/**
 * Multi-value query parameters for CreateFormSchema
 */
export interface CreateFormSchemaRequestArrayParameters {
}

/**
 * Request body parameter for CreateFormSchema
 */
export type CreateFormSchemaRequestBody = FormSchemaInput;

// Type that the handler function provided to the wrapper must conform to
type CreateFormSchemaHandlerFunction<ApiError> = LambdaHandlerFunction<CreateFormSchemaRequestParameters, CreateFormSchemaRequestArrayParameters, CreateFormSchemaRequestBody, FormSchema, ApiError>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of createFormSchema
 */
export const createFormSchemaHandler = <ApiError>(handler: CreateFormSchemaHandlerFunction<ApiError>): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as CreateFormSchemaRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as CreateFormSchemaRequestArrayParameters;

    const body = parseBody(event.body, ['application/json',]) as CreateFormSchemaRequestBody;

    const response = await handler({
        requestParameters,
        requestArrayParameters,
        body,
    }, event, context);

    return {
        ...response,
        body: response.body ? JSON.stringify(response.body) : '',
    };
};
// Type alias for the request
type DeleteFormSchemaRequestInput = DeleteFormSchemaRequest;

/**
 * Single-value path/query parameters for DeleteFormSchema
 */
export interface DeleteFormSchemaRequestParameters {
    readonly schemaId: string;
}

/**
 * Multi-value query parameters for DeleteFormSchema
 */
export interface DeleteFormSchemaRequestArrayParameters {
}

/**
 * Request body parameter for DeleteFormSchema
 */
export type DeleteFormSchemaRequestBody = never;

// Type that the handler function provided to the wrapper must conform to
type DeleteFormSchemaHandlerFunction<ApiError> = LambdaHandlerFunction<DeleteFormSchemaRequestParameters, DeleteFormSchemaRequestArrayParameters, DeleteFormSchemaRequestBody, FormSchema, ApiError>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of deleteFormSchema
 */
export const deleteFormSchemaHandler = <ApiError>(handler: DeleteFormSchemaHandlerFunction<ApiError>): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as DeleteFormSchemaRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as DeleteFormSchemaRequestArrayParameters;

    const body = parseBody(event.body, ['application/json']) as DeleteFormSchemaRequestBody;

    const response = await handler({
        requestParameters,
        requestArrayParameters,
        body,
    }, event, context);

    return {
        ...response,
        body: response.body ? JSON.stringify(response.body) : '',
    };
};
// Type alias for the request
type GetDocumentRequestInput = GetDocumentRequest;

/**
 * Single-value path/query parameters for GetDocument
 */
export interface GetDocumentRequestParameters {
    readonly documentId: string;
}

/**
 * Multi-value query parameters for GetDocument
 */
export interface GetDocumentRequestArrayParameters {
}

/**
 * Request body parameter for GetDocument
 */
export type GetDocumentRequestBody = never;

// Type that the handler function provided to the wrapper must conform to
type GetDocumentHandlerFunction<ApiError> = LambdaHandlerFunction<GetDocumentRequestParameters, GetDocumentRequestArrayParameters, GetDocumentRequestBody, DocumentMetadata, ApiError>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of getDocument
 */
export const getDocumentHandler = <ApiError>(handler: GetDocumentHandlerFunction<ApiError>): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as GetDocumentRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as GetDocumentRequestArrayParameters;

    const body = parseBody(event.body, ['application/json']) as GetDocumentRequestBody;

    const response = await handler({
        requestParameters,
        requestArrayParameters,
        body,
    }, event, context);

    return {
        ...response,
        body: response.body ? JSON.stringify(response.body) : '',
    };
};
// Type alias for the request
type GetDocumentFormRequestInput = GetDocumentFormRequest;

/**
 * Single-value path/query parameters for GetDocumentForm
 */
export interface GetDocumentFormRequestParameters {
    readonly documentId: string;
    readonly formId: string;
}

/**
 * Multi-value query parameters for GetDocumentForm
 */
export interface GetDocumentFormRequestArrayParameters {
}

/**
 * Request body parameter for GetDocumentForm
 */
export type GetDocumentFormRequestBody = never;

// Type that the handler function provided to the wrapper must conform to
type GetDocumentFormHandlerFunction<ApiError> = LambdaHandlerFunction<GetDocumentFormRequestParameters, GetDocumentFormRequestArrayParameters, GetDocumentFormRequestBody, FormMetadata, ApiError>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of getDocumentForm
 */
export const getDocumentFormHandler = <ApiError>(handler: GetDocumentFormHandlerFunction<ApiError>): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as GetDocumentFormRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as GetDocumentFormRequestArrayParameters;

    const body = parseBody(event.body, ['application/json']) as GetDocumentFormRequestBody;

    const response = await handler({
        requestParameters,
        requestArrayParameters,
        body,
    }, event, context);

    return {
        ...response,
        body: response.body ? JSON.stringify(response.body) : '',
    };
};
// Type alias for the request
type GetDocumentUploadUrlRequestInput = GetDocumentUploadUrlRequest;

/**
 * Single-value path/query parameters for GetDocumentUploadUrl
 */
export interface GetDocumentUploadUrlRequestParameters {
    readonly fileName: string;
    readonly contentType: string;
}

/**
 * Multi-value query parameters for GetDocumentUploadUrl
 */
export interface GetDocumentUploadUrlRequestArrayParameters {
}

/**
 * Request body parameter for GetDocumentUploadUrl
 */
export type GetDocumentUploadUrlRequestBody = never;

// Type that the handler function provided to the wrapper must conform to
type GetDocumentUploadUrlHandlerFunction<ApiError> = LambdaHandlerFunction<GetDocumentUploadUrlRequestParameters, GetDocumentUploadUrlRequestArrayParameters, GetDocumentUploadUrlRequestBody, GetDocumentUploadUrlResponse, ApiError>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of getDocumentUploadUrl
 */
export const getDocumentUploadUrlHandler = <ApiError>(handler: GetDocumentUploadUrlHandlerFunction<ApiError>): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as GetDocumentUploadUrlRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as GetDocumentUploadUrlRequestArrayParameters;

    const body = parseBody(event.body, ['application/json']) as GetDocumentUploadUrlRequestBody;

    const response = await handler({
        requestParameters,
        requestArrayParameters,
        body,
    }, event, context);

    return {
        ...response,
        body: response.body ? JSON.stringify(response.body) : '',
    };
};
// Type alias for the request
type GetFormSchemaRequestInput = GetFormSchemaRequest;

/**
 * Single-value path/query parameters for GetFormSchema
 */
export interface GetFormSchemaRequestParameters {
    readonly schemaId: string;
}

/**
 * Multi-value query parameters for GetFormSchema
 */
export interface GetFormSchemaRequestArrayParameters {
}

/**
 * Request body parameter for GetFormSchema
 */
export type GetFormSchemaRequestBody = never;

// Type that the handler function provided to the wrapper must conform to
type GetFormSchemaHandlerFunction<ApiError> = LambdaHandlerFunction<GetFormSchemaRequestParameters, GetFormSchemaRequestArrayParameters, GetFormSchemaRequestBody, FormSchema, ApiError>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of getFormSchema
 */
export const getFormSchemaHandler = <ApiError>(handler: GetFormSchemaHandlerFunction<ApiError>): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as GetFormSchemaRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as GetFormSchemaRequestArrayParameters;

    const body = parseBody(event.body, ['application/json']) as GetFormSchemaRequestBody;

    const response = await handler({
        requestParameters,
        requestArrayParameters,
        body,
    }, event, context);

    return {
        ...response,
        body: response.body ? JSON.stringify(response.body) : '',
    };
};
// Type alias for the request
type GetMetricsRequestInput = GetMetricsRequest;

/**
 * Single-value path/query parameters for GetMetrics
 */
export interface GetMetricsRequestParameters {
    readonly startTimestamp: string;
    readonly endTimestamp: string;
}

/**
 * Multi-value query parameters for GetMetrics
 */
export interface GetMetricsRequestArrayParameters {
}

/**
 * Request body parameter for GetMetrics
 */
export type GetMetricsRequestBody = never;

// Type that the handler function provided to the wrapper must conform to
type GetMetricsHandlerFunction<ApiError> = LambdaHandlerFunction<GetMetricsRequestParameters, GetMetricsRequestArrayParameters, GetMetricsRequestBody, AggregateMetrics, ApiError>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of getMetrics
 */
export const getMetricsHandler = <ApiError>(handler: GetMetricsHandlerFunction<ApiError>): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as GetMetricsRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as GetMetricsRequestArrayParameters;

    const body = parseBody(event.body, ['application/json']) as GetMetricsRequestBody;

    const response = await handler({
        requestParameters,
        requestArrayParameters,
        body,
    }, event, context);

    return {
        ...response,
        body: response.body ? JSON.stringify(response.body) : '',
    };
};
// Type alias for the request
type ListDocumentFormsRequestInput = ListDocumentFormsRequest;

/**
 * Single-value path/query parameters for ListDocumentForms
 */
export interface ListDocumentFormsRequestParameters {
    readonly documentId: string;
    readonly pageSize: string;
    readonly nextToken?: string;
}

/**
 * Multi-value query parameters for ListDocumentForms
 */
export interface ListDocumentFormsRequestArrayParameters {
}

/**
 * Request body parameter for ListDocumentForms
 */
export type ListDocumentFormsRequestBody = never;

// Type that the handler function provided to the wrapper must conform to
type ListDocumentFormsHandlerFunction<ApiError> = LambdaHandlerFunction<ListDocumentFormsRequestParameters, ListDocumentFormsRequestArrayParameters, ListDocumentFormsRequestBody, ListFormsResponse, ApiError>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of listDocumentForms
 */
export const listDocumentFormsHandler = <ApiError>(handler: ListDocumentFormsHandlerFunction<ApiError>): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as ListDocumentFormsRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as ListDocumentFormsRequestArrayParameters;

    const body = parseBody(event.body, ['application/json']) as ListDocumentFormsRequestBody;

    const response = await handler({
        requestParameters,
        requestArrayParameters,
        body,
    }, event, context);

    return {
        ...response,
        body: response.body ? JSON.stringify(response.body) : '',
    };
};
// Type alias for the request
type ListDocumentsRequestInput = ListDocumentsRequest;

/**
 * Single-value path/query parameters for ListDocuments
 */
export interface ListDocumentsRequestParameters {
    readonly pageSize: string;
    readonly nextToken?: string;
}

/**
 * Multi-value query parameters for ListDocuments
 */
export interface ListDocumentsRequestArrayParameters {
}

/**
 * Request body parameter for ListDocuments
 */
export type ListDocumentsRequestBody = never;

// Type that the handler function provided to the wrapper must conform to
type ListDocumentsHandlerFunction<ApiError> = LambdaHandlerFunction<ListDocumentsRequestParameters, ListDocumentsRequestArrayParameters, ListDocumentsRequestBody, ListDocumentsResponse, ApiError>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of listDocuments
 */
export const listDocumentsHandler = <ApiError>(handler: ListDocumentsHandlerFunction<ApiError>): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as ListDocumentsRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as ListDocumentsRequestArrayParameters;

    const body = parseBody(event.body, ['application/json']) as ListDocumentsRequestBody;

    const response = await handler({
        requestParameters,
        requestArrayParameters,
        body,
    }, event, context);

    return {
        ...response,
        body: response.body ? JSON.stringify(response.body) : '',
    };
};
// Type alias for the request
type ListFormReviewWorkflowTagsRequestInput = ListFormReviewWorkflowTagsRequest;

/**
 * Single-value path/query parameters for ListFormReviewWorkflowTags
 */
export interface ListFormReviewWorkflowTagsRequestParameters {
    readonly pageSize: string;
    readonly nextToken?: string;
}

/**
 * Multi-value query parameters for ListFormReviewWorkflowTags
 */
export interface ListFormReviewWorkflowTagsRequestArrayParameters {
}

/**
 * Request body parameter for ListFormReviewWorkflowTags
 */
export type ListFormReviewWorkflowTagsRequestBody = never;

// Type that the handler function provided to the wrapper must conform to
type ListFormReviewWorkflowTagsHandlerFunction<ApiError> = LambdaHandlerFunction<ListFormReviewWorkflowTagsRequestParameters, ListFormReviewWorkflowTagsRequestArrayParameters, ListFormReviewWorkflowTagsRequestBody, ListFormReviewWorkflowTagsResponse, ApiError>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of listFormReviewWorkflowTags
 */
export const listFormReviewWorkflowTagsHandler = <ApiError>(handler: ListFormReviewWorkflowTagsHandlerFunction<ApiError>): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as ListFormReviewWorkflowTagsRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as ListFormReviewWorkflowTagsRequestArrayParameters;

    const body = parseBody(event.body, ['application/json']) as ListFormReviewWorkflowTagsRequestBody;

    const response = await handler({
        requestParameters,
        requestArrayParameters,
        body,
    }, event, context);

    return {
        ...response,
        body: response.body ? JSON.stringify(response.body) : '',
    };
};
// Type alias for the request
type ListFormSchemasRequestInput = ListFormSchemasRequest;

/**
 * Single-value path/query parameters for ListFormSchemas
 */
export interface ListFormSchemasRequestParameters {
    readonly pageSize: string;
    readonly nextToken?: string;
}

/**
 * Multi-value query parameters for ListFormSchemas
 */
export interface ListFormSchemasRequestArrayParameters {
}

/**
 * Request body parameter for ListFormSchemas
 */
export type ListFormSchemasRequestBody = never;

// Type that the handler function provided to the wrapper must conform to
type ListFormSchemasHandlerFunction<ApiError> = LambdaHandlerFunction<ListFormSchemasRequestParameters, ListFormSchemasRequestArrayParameters, ListFormSchemasRequestBody, ListFormSchemasResponse, ApiError>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of listFormSchemas
 */
export const listFormSchemasHandler = <ApiError>(handler: ListFormSchemasHandlerFunction<ApiError>): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as ListFormSchemasRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as ListFormSchemasRequestArrayParameters;

    const body = parseBody(event.body, ['application/json']) as ListFormSchemasRequestBody;

    const response = await handler({
        requestParameters,
        requestArrayParameters,
        body,
    }, event, context);

    return {
        ...response,
        body: response.body ? JSON.stringify(response.body) : '',
    };
};
// Type alias for the request
type ListFormsRequestInput = ListFormsRequest;

/**
 * Single-value path/query parameters for ListForms
 */
export interface ListFormsRequestParameters {
    readonly pageSize: string;
    readonly nextToken?: string;
}

/**
 * Multi-value query parameters for ListForms
 */
export interface ListFormsRequestArrayParameters {
}

/**
 * Request body parameter for ListForms
 */
export type ListFormsRequestBody = never;

// Type that the handler function provided to the wrapper must conform to
type ListFormsHandlerFunction<ApiError> = LambdaHandlerFunction<ListFormsRequestParameters, ListFormsRequestArrayParameters, ListFormsRequestBody, ListFormsResponse, ApiError>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of listForms
 */
export const listFormsHandler = <ApiError>(handler: ListFormsHandlerFunction<ApiError>): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as ListFormsRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as ListFormsRequestArrayParameters;

    const body = parseBody(event.body, ['application/json']) as ListFormsRequestBody;

    const response = await handler({
        requestParameters,
        requestArrayParameters,
        body,
    }, event, context);

    return {
        ...response,
        body: response.body ? JSON.stringify(response.body) : '',
    };
};
// Type alias for the request
type SubmitSourceDocumentRequestInput = SubmitSourceDocumentRequest;

/**
 * Single-value path/query parameters for SubmitSourceDocument
 */
export interface SubmitSourceDocumentRequestParameters {
}

/**
 * Multi-value query parameters for SubmitSourceDocument
 */
export interface SubmitSourceDocumentRequestArrayParameters {
}

/**
 * Request body parameter for SubmitSourceDocument
 */
export type SubmitSourceDocumentRequestBody = SubmitSourceDocumentInput;

// Type that the handler function provided to the wrapper must conform to
type SubmitSourceDocumentHandlerFunction<ApiError> = LambdaHandlerFunction<SubmitSourceDocumentRequestParameters, SubmitSourceDocumentRequestArrayParameters, SubmitSourceDocumentRequestBody, DocumentMetadata, ApiError>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of submitSourceDocument
 */
export const submitSourceDocumentHandler = <ApiError>(handler: SubmitSourceDocumentHandlerFunction<ApiError>): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as SubmitSourceDocumentRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as SubmitSourceDocumentRequestArrayParameters;

    const body = parseBody(event.body, ['application/json',]) as SubmitSourceDocumentRequestBody;

    const response = await handler({
        requestParameters,
        requestArrayParameters,
        body,
    }, event, context);

    return {
        ...response,
        body: response.body ? JSON.stringify(response.body) : '',
    };
};
// Type alias for the request
type UpdateFormReviewRequestInput = UpdateFormReviewRequest;

/**
 * Single-value path/query parameters for UpdateFormReview
 */
export interface UpdateFormReviewRequestParameters {
    readonly documentId: string;
    readonly formId: string;
}

/**
 * Multi-value query parameters for UpdateFormReview
 */
export interface UpdateFormReviewRequestArrayParameters {
}

/**
 * Request body parameter for UpdateFormReview
 */
export type UpdateFormReviewRequestBody = UpdateFormInput;

// Type that the handler function provided to the wrapper must conform to
type UpdateFormReviewHandlerFunction<ApiError> = LambdaHandlerFunction<UpdateFormReviewRequestParameters, UpdateFormReviewRequestArrayParameters, UpdateFormReviewRequestBody, FormMetadata, ApiError>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of updateFormReview
 */
export const updateFormReviewHandler = <ApiError>(handler: UpdateFormReviewHandlerFunction<ApiError>): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as UpdateFormReviewRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as UpdateFormReviewRequestArrayParameters;

    const body = parseBody(event.body, ['application/json',]) as UpdateFormReviewRequestBody;

    const response = await handler({
        requestParameters,
        requestArrayParameters,
        body,
    }, event, context);

    return {
        ...response,
        body: response.body ? JSON.stringify(response.body) : '',
    };
};
// Type alias for the request
type UpdateFormSchemaRequestInput = UpdateFormSchemaRequest;

/**
 * Single-value path/query parameters for UpdateFormSchema
 */
export interface UpdateFormSchemaRequestParameters {
    readonly schemaId: string;
}

/**
 * Multi-value query parameters for UpdateFormSchema
 */
export interface UpdateFormSchemaRequestArrayParameters {
}

/**
 * Request body parameter for UpdateFormSchema
 */
export type UpdateFormSchemaRequestBody = FormSchema;

// Type that the handler function provided to the wrapper must conform to
type UpdateFormSchemaHandlerFunction<ApiError> = LambdaHandlerFunction<UpdateFormSchemaRequestParameters, UpdateFormSchemaRequestArrayParameters, UpdateFormSchemaRequestBody, FormSchema, ApiError>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of updateFormSchema
 */
export const updateFormSchemaHandler = <ApiError>(handler: UpdateFormSchemaHandlerFunction<ApiError>): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as UpdateFormSchemaRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as UpdateFormSchemaRequestArrayParameters;

    const body = parseBody(event.body, ['application/json',]) as UpdateFormSchemaRequestBody;

    const response = await handler({
        requestParameters,
        requestArrayParameters,
        body,
    }, event, context);

    return {
        ...response,
        body: response.body ? JSON.stringify(response.body) : '',
    };
};
// Type alias for the request
type UpdateStatusRequestInput = UpdateStatusRequest;

/**
 * Single-value path/query parameters for UpdateStatus
 */
export interface UpdateStatusRequestParameters {
    readonly documentId: string;
    readonly formId: string;
}

/**
 * Multi-value query parameters for UpdateStatus
 */
export interface UpdateStatusRequestArrayParameters {
}

/**
 * Request body parameter for UpdateStatus
 */
export type UpdateStatusRequestBody = UpdateStatusInput;

// Type that the handler function provided to the wrapper must conform to
type UpdateStatusHandlerFunction<ApiError> = LambdaHandlerFunction<UpdateStatusRequestParameters, UpdateStatusRequestArrayParameters, UpdateStatusRequestBody, FormMetadata, ApiError>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of updateStatus
 */
export const updateStatusHandler = <ApiError>(handler: UpdateStatusHandlerFunction<ApiError>): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as UpdateStatusRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as UpdateStatusRequestArrayParameters;

    const body = parseBody(event.body, ['application/json',]) as UpdateStatusRequestBody;

    const response = await handler({
        requestParameters,
        requestArrayParameters,
        body,
    }, event, context);

    return {
        ...response,
        body: response.body ? JSON.stringify(response.body) : '',
    };
};
