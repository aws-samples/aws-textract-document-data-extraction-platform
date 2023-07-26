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

// API Gateway Types
import { APIGatewayProxyEvent, APIGatewayProxyResult, Context } from "aws-lambda";

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
const parseBody = (body: string, demarshal: (body: string) => any, contentTypes: string[]): any => contentTypes.filter((contentType) => contentType !== 'application/json').length === 0 ? demarshal(body || '{}') : body;

// Api gateway lambda handler type
type ApiGatewayLambdaHandler = (event: APIGatewayProxyEvent, context: Context) => Promise<APIGatewayProxyResult>;

// Type of the response to be returned by an operation lambda handler
export interface OperationResponse<StatusCode extends number, Body> {
    statusCode: StatusCode;
    headers?: { [key: string]: string };
    body: Body;
}

// Input for a lambda handler for an operation
export type LambdaRequestParameters<RequestParameters, RequestArrayParameters, RequestBody> = {
    requestParameters: RequestParameters,
    requestArrayParameters: RequestArrayParameters,
    body: RequestBody,
};

export type InterceptorContext = { [key: string]: any };

export interface RequestInput<RequestParameters, RequestArrayParameters, RequestBody> {
    input: LambdaRequestParameters<RequestParameters, RequestArrayParameters, RequestBody>;
    event: APIGatewayProxyEvent;
    context: Context;
    interceptorContext: InterceptorContext;
}

export interface ChainedRequestInput<RequestParameters, RequestArrayParameters, RequestBody, Response> extends RequestInput<RequestParameters, RequestArrayParameters, RequestBody> {
    chain: LambdaHandlerChain<RequestParameters, RequestArrayParameters, RequestBody, Response>;
}

/**
 * A lambda handler function which is part of a chain. It may invoke the remainder of the chain via the given chain input
 */
export type ChainedLambdaHandlerFunction<RequestParameters, RequestArrayParameters, RequestBody, Response> = (
  input: ChainedRequestInput<RequestParameters, RequestArrayParameters, RequestBody, Response>,
) => Promise<Response>;

// Type for a lambda handler function to be wrapped
export type LambdaHandlerFunction<RequestParameters, RequestArrayParameters, RequestBody, Response> = (
  input: RequestInput<RequestParameters, RequestArrayParameters, RequestBody>,
) => Promise<Response>;

export interface LambdaHandlerChain<RequestParameters, RequestArrayParameters, RequestBody, Response> {
  next: LambdaHandlerFunction<RequestParameters, RequestArrayParameters, RequestBody, Response>;
}

// Interceptor is a type alias for ChainedLambdaHandlerFunction
export type Interceptor<RequestParameters, RequestArrayParameters, RequestBody, Response> = ChainedLambdaHandlerFunction<RequestParameters, RequestArrayParameters, RequestBody, Response>;

/**
 * Build a chain from the given array of chained lambda handlers
 */
const buildHandlerChain = <RequestParameters, RequestArrayParameters, RequestBody, Response>(
  ...handlers: ChainedLambdaHandlerFunction<RequestParameters, RequestArrayParameters, RequestBody, Response>[]
): LambdaHandlerChain<RequestParameters, RequestArrayParameters, RequestBody, Response> => {
  if (handlers.length === 0) {
    return {
      next: () => {
        throw new Error("No more handlers remain in the chain! The last handler should not call next.");
      }
    };
  }
  const [currentHandler, ...remainingHandlers] = handlers;
  return {
    next: (input) => {
      return currentHandler({
        ...input,
        chain: buildHandlerChain(...remainingHandlers),
      });
    },
  };
};

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

export type CreateFormReviewWorkflowTag200OperationResponse = OperationResponse<200, FormReviewWorkflowTag>;
export type CreateFormReviewWorkflowTagOperationResponses = | CreateFormReviewWorkflowTag200OperationResponse ;

// Type that the handler function provided to the wrapper must conform to
export type CreateFormReviewWorkflowTagHandlerFunction = LambdaHandlerFunction<CreateFormReviewWorkflowTagRequestParameters, CreateFormReviewWorkflowTagRequestArrayParameters, CreateFormReviewWorkflowTagRequestBody, CreateFormReviewWorkflowTagOperationResponses>;
export type CreateFormReviewWorkflowTagChainedHandlerFunction = ChainedLambdaHandlerFunction<CreateFormReviewWorkflowTagRequestParameters, CreateFormReviewWorkflowTagRequestArrayParameters, CreateFormReviewWorkflowTagRequestBody, CreateFormReviewWorkflowTagOperationResponses>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of createFormReviewWorkflowTag
 */
export const createFormReviewWorkflowTagHandler = (
    firstHandler: CreateFormReviewWorkflowTagChainedHandlerFunction,
    ...remainingHandlers: CreateFormReviewWorkflowTagChainedHandlerFunction[]
): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as CreateFormReviewWorkflowTagRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as CreateFormReviewWorkflowTagRequestArrayParameters;

    const demarshal = (bodyString: string): any => {
        let parsed = JSON.parse(bodyString);
        parsed = CreateFormReviewWorkflowTagInputFromJSON(parsed);
        return parsed;
    };
    const body = parseBody(event.body, demarshal, ['application/json',]) as CreateFormReviewWorkflowTagRequestBody;

    const chain = buildHandlerChain(firstHandler, ...remainingHandlers);
    const response = await chain.next({
        input: {
            requestParameters,
            requestArrayParameters,
            body,
        },
        event,
        context,
        interceptorContext: {},
    });

    const marshal = (statusCode: number, responseBody: any): string => {
        let marshalledBody = responseBody;
        switch(statusCode) {
            case 200:
                marshalledBody = JSON.stringify(FormReviewWorkflowTagToJSON(marshalledBody));
                break;
            default:
                break;
        }

        return marshalledBody;
    };

    return {
        ...response,
        body: response.body ? marshal(response.statusCode, response.body) : '',
    };
};
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

export type CreateFormSchema200OperationResponse = OperationResponse<200, FormSchema>;
export type CreateFormSchemaOperationResponses = | CreateFormSchema200OperationResponse ;

// Type that the handler function provided to the wrapper must conform to
export type CreateFormSchemaHandlerFunction = LambdaHandlerFunction<CreateFormSchemaRequestParameters, CreateFormSchemaRequestArrayParameters, CreateFormSchemaRequestBody, CreateFormSchemaOperationResponses>;
export type CreateFormSchemaChainedHandlerFunction = ChainedLambdaHandlerFunction<CreateFormSchemaRequestParameters, CreateFormSchemaRequestArrayParameters, CreateFormSchemaRequestBody, CreateFormSchemaOperationResponses>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of createFormSchema
 */
export const createFormSchemaHandler = (
    firstHandler: CreateFormSchemaChainedHandlerFunction,
    ...remainingHandlers: CreateFormSchemaChainedHandlerFunction[]
): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as CreateFormSchemaRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as CreateFormSchemaRequestArrayParameters;

    const demarshal = (bodyString: string): any => {
        let parsed = JSON.parse(bodyString);
        parsed = FormSchemaInputFromJSON(parsed);
        return parsed;
    };
    const body = parseBody(event.body, demarshal, ['application/json',]) as CreateFormSchemaRequestBody;

    const chain = buildHandlerChain(firstHandler, ...remainingHandlers);
    const response = await chain.next({
        input: {
            requestParameters,
            requestArrayParameters,
            body,
        },
        event,
        context,
        interceptorContext: {},
    });

    const marshal = (statusCode: number, responseBody: any): string => {
        let marshalledBody = responseBody;
        switch(statusCode) {
            case 200:
                marshalledBody = JSON.stringify(FormSchemaToJSON(marshalledBody));
                break;
            default:
                break;
        }

        return marshalledBody;
    };

    return {
        ...response,
        body: response.body ? marshal(response.statusCode, response.body) : '',
    };
};
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

export type DeleteFormSchema200OperationResponse = OperationResponse<200, FormSchema>;
export type DeleteFormSchemaOperationResponses = | DeleteFormSchema200OperationResponse ;

// Type that the handler function provided to the wrapper must conform to
export type DeleteFormSchemaHandlerFunction = LambdaHandlerFunction<DeleteFormSchemaRequestParameters, DeleteFormSchemaRequestArrayParameters, DeleteFormSchemaRequestBody, DeleteFormSchemaOperationResponses>;
export type DeleteFormSchemaChainedHandlerFunction = ChainedLambdaHandlerFunction<DeleteFormSchemaRequestParameters, DeleteFormSchemaRequestArrayParameters, DeleteFormSchemaRequestBody, DeleteFormSchemaOperationResponses>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of deleteFormSchema
 */
export const deleteFormSchemaHandler = (
    firstHandler: DeleteFormSchemaChainedHandlerFunction,
    ...remainingHandlers: DeleteFormSchemaChainedHandlerFunction[]
): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as DeleteFormSchemaRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as DeleteFormSchemaRequestArrayParameters;

    const demarshal = (bodyString: string): any => {
        let parsed = JSON.parse(bodyString);
        return parsed;
    };
    const body = parseBody(event.body, demarshal, ['application/json']) as DeleteFormSchemaRequestBody;

    const chain = buildHandlerChain(firstHandler, ...remainingHandlers);
    const response = await chain.next({
        input: {
            requestParameters,
            requestArrayParameters,
            body,
        },
        event,
        context,
        interceptorContext: {},
    });

    const marshal = (statusCode: number, responseBody: any): string => {
        let marshalledBody = responseBody;
        switch(statusCode) {
            case 200:
                marshalledBody = JSON.stringify(FormSchemaToJSON(marshalledBody));
                break;
            default:
                break;
        }

        return marshalledBody;
    };

    return {
        ...response,
        body: response.body ? marshal(response.statusCode, response.body) : '',
    };
};
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

export type GetDocument200OperationResponse = OperationResponse<200, DocumentMetadata>;
export type GetDocument404OperationResponse = OperationResponse<404, ApiError>;
export type GetDocumentOperationResponses = | GetDocument200OperationResponse | GetDocument404OperationResponse ;

// Type that the handler function provided to the wrapper must conform to
export type GetDocumentHandlerFunction = LambdaHandlerFunction<GetDocumentRequestParameters, GetDocumentRequestArrayParameters, GetDocumentRequestBody, GetDocumentOperationResponses>;
export type GetDocumentChainedHandlerFunction = ChainedLambdaHandlerFunction<GetDocumentRequestParameters, GetDocumentRequestArrayParameters, GetDocumentRequestBody, GetDocumentOperationResponses>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of getDocument
 */
export const getDocumentHandler = (
    firstHandler: GetDocumentChainedHandlerFunction,
    ...remainingHandlers: GetDocumentChainedHandlerFunction[]
): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as GetDocumentRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as GetDocumentRequestArrayParameters;

    const demarshal = (bodyString: string): any => {
        let parsed = JSON.parse(bodyString);
        return parsed;
    };
    const body = parseBody(event.body, demarshal, ['application/json']) as GetDocumentRequestBody;

    const chain = buildHandlerChain(firstHandler, ...remainingHandlers);
    const response = await chain.next({
        input: {
            requestParameters,
            requestArrayParameters,
            body,
        },
        event,
        context,
        interceptorContext: {},
    });

    const marshal = (statusCode: number, responseBody: any): string => {
        let marshalledBody = responseBody;
        switch(statusCode) {
            case 200:
                marshalledBody = JSON.stringify(DocumentMetadataToJSON(marshalledBody));
                break;
            case 404:
                marshalledBody = JSON.stringify(ApiErrorToJSON(marshalledBody));
                break;
            default:
                break;
        }

        return marshalledBody;
    };

    return {
        ...response,
        body: response.body ? marshal(response.statusCode, response.body) : '',
    };
};
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

export type GetDocumentForm200OperationResponse = OperationResponse<200, FormMetadata>;
export type GetDocumentForm404OperationResponse = OperationResponse<404, ApiError>;
export type GetDocumentFormOperationResponses = | GetDocumentForm200OperationResponse | GetDocumentForm404OperationResponse ;

// Type that the handler function provided to the wrapper must conform to
export type GetDocumentFormHandlerFunction = LambdaHandlerFunction<GetDocumentFormRequestParameters, GetDocumentFormRequestArrayParameters, GetDocumentFormRequestBody, GetDocumentFormOperationResponses>;
export type GetDocumentFormChainedHandlerFunction = ChainedLambdaHandlerFunction<GetDocumentFormRequestParameters, GetDocumentFormRequestArrayParameters, GetDocumentFormRequestBody, GetDocumentFormOperationResponses>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of getDocumentForm
 */
export const getDocumentFormHandler = (
    firstHandler: GetDocumentFormChainedHandlerFunction,
    ...remainingHandlers: GetDocumentFormChainedHandlerFunction[]
): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as GetDocumentFormRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as GetDocumentFormRequestArrayParameters;

    const demarshal = (bodyString: string): any => {
        let parsed = JSON.parse(bodyString);
        return parsed;
    };
    const body = parseBody(event.body, demarshal, ['application/json']) as GetDocumentFormRequestBody;

    const chain = buildHandlerChain(firstHandler, ...remainingHandlers);
    const response = await chain.next({
        input: {
            requestParameters,
            requestArrayParameters,
            body,
        },
        event,
        context,
        interceptorContext: {},
    });

    const marshal = (statusCode: number, responseBody: any): string => {
        let marshalledBody = responseBody;
        switch(statusCode) {
            case 200:
                marshalledBody = JSON.stringify(FormMetadataToJSON(marshalledBody));
                break;
            case 404:
                marshalledBody = JSON.stringify(ApiErrorToJSON(marshalledBody));
                break;
            default:
                break;
        }

        return marshalledBody;
    };

    return {
        ...response,
        body: response.body ? marshal(response.statusCode, response.body) : '',
    };
};
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

export type GetDocumentUploadUrl200OperationResponse = OperationResponse<200, GetDocumentUploadUrlResponse>;
export type GetDocumentUploadUrlOperationResponses = | GetDocumentUploadUrl200OperationResponse ;

// Type that the handler function provided to the wrapper must conform to
export type GetDocumentUploadUrlHandlerFunction = LambdaHandlerFunction<GetDocumentUploadUrlRequestParameters, GetDocumentUploadUrlRequestArrayParameters, GetDocumentUploadUrlRequestBody, GetDocumentUploadUrlOperationResponses>;
export type GetDocumentUploadUrlChainedHandlerFunction = ChainedLambdaHandlerFunction<GetDocumentUploadUrlRequestParameters, GetDocumentUploadUrlRequestArrayParameters, GetDocumentUploadUrlRequestBody, GetDocumentUploadUrlOperationResponses>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of getDocumentUploadUrl
 */
export const getDocumentUploadUrlHandler = (
    firstHandler: GetDocumentUploadUrlChainedHandlerFunction,
    ...remainingHandlers: GetDocumentUploadUrlChainedHandlerFunction[]
): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as GetDocumentUploadUrlRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as GetDocumentUploadUrlRequestArrayParameters;

    const demarshal = (bodyString: string): any => {
        let parsed = JSON.parse(bodyString);
        return parsed;
    };
    const body = parseBody(event.body, demarshal, ['application/json']) as GetDocumentUploadUrlRequestBody;

    const chain = buildHandlerChain(firstHandler, ...remainingHandlers);
    const response = await chain.next({
        input: {
            requestParameters,
            requestArrayParameters,
            body,
        },
        event,
        context,
        interceptorContext: {},
    });

    const marshal = (statusCode: number, responseBody: any): string => {
        let marshalledBody = responseBody;
        switch(statusCode) {
            case 200:
                marshalledBody = JSON.stringify(GetDocumentUploadUrlResponseToJSON(marshalledBody));
                break;
            default:
                break;
        }

        return marshalledBody;
    };

    return {
        ...response,
        body: response.body ? marshal(response.statusCode, response.body) : '',
    };
};
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

export type GetFormSchema200OperationResponse = OperationResponse<200, FormSchema>;
export type GetFormSchemaOperationResponses = | GetFormSchema200OperationResponse ;

// Type that the handler function provided to the wrapper must conform to
export type GetFormSchemaHandlerFunction = LambdaHandlerFunction<GetFormSchemaRequestParameters, GetFormSchemaRequestArrayParameters, GetFormSchemaRequestBody, GetFormSchemaOperationResponses>;
export type GetFormSchemaChainedHandlerFunction = ChainedLambdaHandlerFunction<GetFormSchemaRequestParameters, GetFormSchemaRequestArrayParameters, GetFormSchemaRequestBody, GetFormSchemaOperationResponses>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of getFormSchema
 */
export const getFormSchemaHandler = (
    firstHandler: GetFormSchemaChainedHandlerFunction,
    ...remainingHandlers: GetFormSchemaChainedHandlerFunction[]
): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as GetFormSchemaRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as GetFormSchemaRequestArrayParameters;

    const demarshal = (bodyString: string): any => {
        let parsed = JSON.parse(bodyString);
        return parsed;
    };
    const body = parseBody(event.body, demarshal, ['application/json']) as GetFormSchemaRequestBody;

    const chain = buildHandlerChain(firstHandler, ...remainingHandlers);
    const response = await chain.next({
        input: {
            requestParameters,
            requestArrayParameters,
            body,
        },
        event,
        context,
        interceptorContext: {},
    });

    const marshal = (statusCode: number, responseBody: any): string => {
        let marshalledBody = responseBody;
        switch(statusCode) {
            case 200:
                marshalledBody = JSON.stringify(FormSchemaToJSON(marshalledBody));
                break;
            default:
                break;
        }

        return marshalledBody;
    };

    return {
        ...response,
        body: response.body ? marshal(response.statusCode, response.body) : '',
    };
};
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

export type GetMetrics200OperationResponse = OperationResponse<200, AggregateMetrics>;
export type GetMetricsOperationResponses = | GetMetrics200OperationResponse ;

// Type that the handler function provided to the wrapper must conform to
export type GetMetricsHandlerFunction = LambdaHandlerFunction<GetMetricsRequestParameters, GetMetricsRequestArrayParameters, GetMetricsRequestBody, GetMetricsOperationResponses>;
export type GetMetricsChainedHandlerFunction = ChainedLambdaHandlerFunction<GetMetricsRequestParameters, GetMetricsRequestArrayParameters, GetMetricsRequestBody, GetMetricsOperationResponses>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of getMetrics
 */
export const getMetricsHandler = (
    firstHandler: GetMetricsChainedHandlerFunction,
    ...remainingHandlers: GetMetricsChainedHandlerFunction[]
): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as GetMetricsRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as GetMetricsRequestArrayParameters;

    const demarshal = (bodyString: string): any => {
        let parsed = JSON.parse(bodyString);
        return parsed;
    };
    const body = parseBody(event.body, demarshal, ['application/json']) as GetMetricsRequestBody;

    const chain = buildHandlerChain(firstHandler, ...remainingHandlers);
    const response = await chain.next({
        input: {
            requestParameters,
            requestArrayParameters,
            body,
        },
        event,
        context,
        interceptorContext: {},
    });

    const marshal = (statusCode: number, responseBody: any): string => {
        let marshalledBody = responseBody;
        switch(statusCode) {
            case 200:
                marshalledBody = JSON.stringify(AggregateMetricsToJSON(marshalledBody));
                break;
            default:
                break;
        }

        return marshalledBody;
    };

    return {
        ...response,
        body: response.body ? marshal(response.statusCode, response.body) : '',
    };
};
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

export type ListDocumentForms200OperationResponse = OperationResponse<200, ListFormsResponse>;
export type ListDocumentForms404OperationResponse = OperationResponse<404, ApiError>;
export type ListDocumentFormsOperationResponses = | ListDocumentForms200OperationResponse | ListDocumentForms404OperationResponse ;

// Type that the handler function provided to the wrapper must conform to
export type ListDocumentFormsHandlerFunction = LambdaHandlerFunction<ListDocumentFormsRequestParameters, ListDocumentFormsRequestArrayParameters, ListDocumentFormsRequestBody, ListDocumentFormsOperationResponses>;
export type ListDocumentFormsChainedHandlerFunction = ChainedLambdaHandlerFunction<ListDocumentFormsRequestParameters, ListDocumentFormsRequestArrayParameters, ListDocumentFormsRequestBody, ListDocumentFormsOperationResponses>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of listDocumentForms
 */
export const listDocumentFormsHandler = (
    firstHandler: ListDocumentFormsChainedHandlerFunction,
    ...remainingHandlers: ListDocumentFormsChainedHandlerFunction[]
): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as ListDocumentFormsRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as ListDocumentFormsRequestArrayParameters;

    const demarshal = (bodyString: string): any => {
        let parsed = JSON.parse(bodyString);
        return parsed;
    };
    const body = parseBody(event.body, demarshal, ['application/json']) as ListDocumentFormsRequestBody;

    const chain = buildHandlerChain(firstHandler, ...remainingHandlers);
    const response = await chain.next({
        input: {
            requestParameters,
            requestArrayParameters,
            body,
        },
        event,
        context,
        interceptorContext: {},
    });

    const marshal = (statusCode: number, responseBody: any): string => {
        let marshalledBody = responseBody;
        switch(statusCode) {
            case 200:
                marshalledBody = JSON.stringify(ListFormsResponseToJSON(marshalledBody));
                break;
            case 404:
                marshalledBody = JSON.stringify(ApiErrorToJSON(marshalledBody));
                break;
            default:
                break;
        }

        return marshalledBody;
    };

    return {
        ...response,
        body: response.body ? marshal(response.statusCode, response.body) : '',
    };
};
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

export type ListDocuments200OperationResponse = OperationResponse<200, ListDocumentsResponse>;
export type ListDocumentsOperationResponses = | ListDocuments200OperationResponse ;

// Type that the handler function provided to the wrapper must conform to
export type ListDocumentsHandlerFunction = LambdaHandlerFunction<ListDocumentsRequestParameters, ListDocumentsRequestArrayParameters, ListDocumentsRequestBody, ListDocumentsOperationResponses>;
export type ListDocumentsChainedHandlerFunction = ChainedLambdaHandlerFunction<ListDocumentsRequestParameters, ListDocumentsRequestArrayParameters, ListDocumentsRequestBody, ListDocumentsOperationResponses>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of listDocuments
 */
export const listDocumentsHandler = (
    firstHandler: ListDocumentsChainedHandlerFunction,
    ...remainingHandlers: ListDocumentsChainedHandlerFunction[]
): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as ListDocumentsRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as ListDocumentsRequestArrayParameters;

    const demarshal = (bodyString: string): any => {
        let parsed = JSON.parse(bodyString);
        return parsed;
    };
    const body = parseBody(event.body, demarshal, ['application/json']) as ListDocumentsRequestBody;

    const chain = buildHandlerChain(firstHandler, ...remainingHandlers);
    const response = await chain.next({
        input: {
            requestParameters,
            requestArrayParameters,
            body,
        },
        event,
        context,
        interceptorContext: {},
    });

    const marshal = (statusCode: number, responseBody: any): string => {
        let marshalledBody = responseBody;
        switch(statusCode) {
            case 200:
                marshalledBody = JSON.stringify(ListDocumentsResponseToJSON(marshalledBody));
                break;
            default:
                break;
        }

        return marshalledBody;
    };

    return {
        ...response,
        body: response.body ? marshal(response.statusCode, response.body) : '',
    };
};
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

export type ListFormReviewWorkflowTags200OperationResponse = OperationResponse<200, ListFormReviewWorkflowTagsResponse>;
export type ListFormReviewWorkflowTagsOperationResponses = | ListFormReviewWorkflowTags200OperationResponse ;

// Type that the handler function provided to the wrapper must conform to
export type ListFormReviewWorkflowTagsHandlerFunction = LambdaHandlerFunction<ListFormReviewWorkflowTagsRequestParameters, ListFormReviewWorkflowTagsRequestArrayParameters, ListFormReviewWorkflowTagsRequestBody, ListFormReviewWorkflowTagsOperationResponses>;
export type ListFormReviewWorkflowTagsChainedHandlerFunction = ChainedLambdaHandlerFunction<ListFormReviewWorkflowTagsRequestParameters, ListFormReviewWorkflowTagsRequestArrayParameters, ListFormReviewWorkflowTagsRequestBody, ListFormReviewWorkflowTagsOperationResponses>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of listFormReviewWorkflowTags
 */
export const listFormReviewWorkflowTagsHandler = (
    firstHandler: ListFormReviewWorkflowTagsChainedHandlerFunction,
    ...remainingHandlers: ListFormReviewWorkflowTagsChainedHandlerFunction[]
): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as ListFormReviewWorkflowTagsRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as ListFormReviewWorkflowTagsRequestArrayParameters;

    const demarshal = (bodyString: string): any => {
        let parsed = JSON.parse(bodyString);
        return parsed;
    };
    const body = parseBody(event.body, demarshal, ['application/json']) as ListFormReviewWorkflowTagsRequestBody;

    const chain = buildHandlerChain(firstHandler, ...remainingHandlers);
    const response = await chain.next({
        input: {
            requestParameters,
            requestArrayParameters,
            body,
        },
        event,
        context,
        interceptorContext: {},
    });

    const marshal = (statusCode: number, responseBody: any): string => {
        let marshalledBody = responseBody;
        switch(statusCode) {
            case 200:
                marshalledBody = JSON.stringify(ListFormReviewWorkflowTagsResponseToJSON(marshalledBody));
                break;
            default:
                break;
        }

        return marshalledBody;
    };

    return {
        ...response,
        body: response.body ? marshal(response.statusCode, response.body) : '',
    };
};
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

export type ListFormSchemas200OperationResponse = OperationResponse<200, ListFormSchemasResponse>;
export type ListFormSchemasOperationResponses = | ListFormSchemas200OperationResponse ;

// Type that the handler function provided to the wrapper must conform to
export type ListFormSchemasHandlerFunction = LambdaHandlerFunction<ListFormSchemasRequestParameters, ListFormSchemasRequestArrayParameters, ListFormSchemasRequestBody, ListFormSchemasOperationResponses>;
export type ListFormSchemasChainedHandlerFunction = ChainedLambdaHandlerFunction<ListFormSchemasRequestParameters, ListFormSchemasRequestArrayParameters, ListFormSchemasRequestBody, ListFormSchemasOperationResponses>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of listFormSchemas
 */
export const listFormSchemasHandler = (
    firstHandler: ListFormSchemasChainedHandlerFunction,
    ...remainingHandlers: ListFormSchemasChainedHandlerFunction[]
): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as ListFormSchemasRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as ListFormSchemasRequestArrayParameters;

    const demarshal = (bodyString: string): any => {
        let parsed = JSON.parse(bodyString);
        return parsed;
    };
    const body = parseBody(event.body, demarshal, ['application/json']) as ListFormSchemasRequestBody;

    const chain = buildHandlerChain(firstHandler, ...remainingHandlers);
    const response = await chain.next({
        input: {
            requestParameters,
            requestArrayParameters,
            body,
        },
        event,
        context,
        interceptorContext: {},
    });

    const marshal = (statusCode: number, responseBody: any): string => {
        let marshalledBody = responseBody;
        switch(statusCode) {
            case 200:
                marshalledBody = JSON.stringify(ListFormSchemasResponseToJSON(marshalledBody));
                break;
            default:
                break;
        }

        return marshalledBody;
    };

    return {
        ...response,
        body: response.body ? marshal(response.statusCode, response.body) : '',
    };
};
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

export type ListForms200OperationResponse = OperationResponse<200, ListFormsResponse>;
export type ListFormsOperationResponses = | ListForms200OperationResponse ;

// Type that the handler function provided to the wrapper must conform to
export type ListFormsHandlerFunction = LambdaHandlerFunction<ListFormsRequestParameters, ListFormsRequestArrayParameters, ListFormsRequestBody, ListFormsOperationResponses>;
export type ListFormsChainedHandlerFunction = ChainedLambdaHandlerFunction<ListFormsRequestParameters, ListFormsRequestArrayParameters, ListFormsRequestBody, ListFormsOperationResponses>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of listForms
 */
export const listFormsHandler = (
    firstHandler: ListFormsChainedHandlerFunction,
    ...remainingHandlers: ListFormsChainedHandlerFunction[]
): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as ListFormsRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as ListFormsRequestArrayParameters;

    const demarshal = (bodyString: string): any => {
        let parsed = JSON.parse(bodyString);
        return parsed;
    };
    const body = parseBody(event.body, demarshal, ['application/json']) as ListFormsRequestBody;

    const chain = buildHandlerChain(firstHandler, ...remainingHandlers);
    const response = await chain.next({
        input: {
            requestParameters,
            requestArrayParameters,
            body,
        },
        event,
        context,
        interceptorContext: {},
    });

    const marshal = (statusCode: number, responseBody: any): string => {
        let marshalledBody = responseBody;
        switch(statusCode) {
            case 200:
                marshalledBody = JSON.stringify(ListFormsResponseToJSON(marshalledBody));
                break;
            default:
                break;
        }

        return marshalledBody;
    };

    return {
        ...response,
        body: response.body ? marshal(response.statusCode, response.body) : '',
    };
};
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

export type SubmitSourceDocument200OperationResponse = OperationResponse<200, DocumentMetadata>;
export type SubmitSourceDocumentOperationResponses = | SubmitSourceDocument200OperationResponse ;

// Type that the handler function provided to the wrapper must conform to
export type SubmitSourceDocumentHandlerFunction = LambdaHandlerFunction<SubmitSourceDocumentRequestParameters, SubmitSourceDocumentRequestArrayParameters, SubmitSourceDocumentRequestBody, SubmitSourceDocumentOperationResponses>;
export type SubmitSourceDocumentChainedHandlerFunction = ChainedLambdaHandlerFunction<SubmitSourceDocumentRequestParameters, SubmitSourceDocumentRequestArrayParameters, SubmitSourceDocumentRequestBody, SubmitSourceDocumentOperationResponses>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of submitSourceDocument
 */
export const submitSourceDocumentHandler = (
    firstHandler: SubmitSourceDocumentChainedHandlerFunction,
    ...remainingHandlers: SubmitSourceDocumentChainedHandlerFunction[]
): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as SubmitSourceDocumentRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as SubmitSourceDocumentRequestArrayParameters;

    const demarshal = (bodyString: string): any => {
        let parsed = JSON.parse(bodyString);
        parsed = SubmitSourceDocumentInputFromJSON(parsed);
        return parsed;
    };
    const body = parseBody(event.body, demarshal, ['application/json',]) as SubmitSourceDocumentRequestBody;

    const chain = buildHandlerChain(firstHandler, ...remainingHandlers);
    const response = await chain.next({
        input: {
            requestParameters,
            requestArrayParameters,
            body,
        },
        event,
        context,
        interceptorContext: {},
    });

    const marshal = (statusCode: number, responseBody: any): string => {
        let marshalledBody = responseBody;
        switch(statusCode) {
            case 200:
                marshalledBody = JSON.stringify(DocumentMetadataToJSON(marshalledBody));
                break;
            default:
                break;
        }

        return marshalledBody;
    };

    return {
        ...response,
        body: response.body ? marshal(response.statusCode, response.body) : '',
    };
};
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

export type UpdateFormReview200OperationResponse = OperationResponse<200, FormMetadata>;
export type UpdateFormReview404OperationResponse = OperationResponse<404, ApiError>;
export type UpdateFormReviewOperationResponses = | UpdateFormReview200OperationResponse | UpdateFormReview404OperationResponse ;

// Type that the handler function provided to the wrapper must conform to
export type UpdateFormReviewHandlerFunction = LambdaHandlerFunction<UpdateFormReviewRequestParameters, UpdateFormReviewRequestArrayParameters, UpdateFormReviewRequestBody, UpdateFormReviewOperationResponses>;
export type UpdateFormReviewChainedHandlerFunction = ChainedLambdaHandlerFunction<UpdateFormReviewRequestParameters, UpdateFormReviewRequestArrayParameters, UpdateFormReviewRequestBody, UpdateFormReviewOperationResponses>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of updateFormReview
 */
export const updateFormReviewHandler = (
    firstHandler: UpdateFormReviewChainedHandlerFunction,
    ...remainingHandlers: UpdateFormReviewChainedHandlerFunction[]
): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as UpdateFormReviewRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as UpdateFormReviewRequestArrayParameters;

    const demarshal = (bodyString: string): any => {
        let parsed = JSON.parse(bodyString);
        parsed = UpdateFormInputFromJSON(parsed);
        return parsed;
    };
    const body = parseBody(event.body, demarshal, ['application/json',]) as UpdateFormReviewRequestBody;

    const chain = buildHandlerChain(firstHandler, ...remainingHandlers);
    const response = await chain.next({
        input: {
            requestParameters,
            requestArrayParameters,
            body,
        },
        event,
        context,
        interceptorContext: {},
    });

    const marshal = (statusCode: number, responseBody: any): string => {
        let marshalledBody = responseBody;
        switch(statusCode) {
            case 200:
                marshalledBody = JSON.stringify(FormMetadataToJSON(marshalledBody));
                break;
            case 404:
                marshalledBody = JSON.stringify(ApiErrorToJSON(marshalledBody));
                break;
            default:
                break;
        }

        return marshalledBody;
    };

    return {
        ...response,
        body: response.body ? marshal(response.statusCode, response.body) : '',
    };
};
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

export type UpdateFormSchema200OperationResponse = OperationResponse<200, FormSchema>;
export type UpdateFormSchemaOperationResponses = | UpdateFormSchema200OperationResponse ;

// Type that the handler function provided to the wrapper must conform to
export type UpdateFormSchemaHandlerFunction = LambdaHandlerFunction<UpdateFormSchemaRequestParameters, UpdateFormSchemaRequestArrayParameters, UpdateFormSchemaRequestBody, UpdateFormSchemaOperationResponses>;
export type UpdateFormSchemaChainedHandlerFunction = ChainedLambdaHandlerFunction<UpdateFormSchemaRequestParameters, UpdateFormSchemaRequestArrayParameters, UpdateFormSchemaRequestBody, UpdateFormSchemaOperationResponses>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of updateFormSchema
 */
export const updateFormSchemaHandler = (
    firstHandler: UpdateFormSchemaChainedHandlerFunction,
    ...remainingHandlers: UpdateFormSchemaChainedHandlerFunction[]
): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as UpdateFormSchemaRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as UpdateFormSchemaRequestArrayParameters;

    const demarshal = (bodyString: string): any => {
        let parsed = JSON.parse(bodyString);
        parsed = FormSchemaFromJSON(parsed);
        return parsed;
    };
    const body = parseBody(event.body, demarshal, ['application/json',]) as UpdateFormSchemaRequestBody;

    const chain = buildHandlerChain(firstHandler, ...remainingHandlers);
    const response = await chain.next({
        input: {
            requestParameters,
            requestArrayParameters,
            body,
        },
        event,
        context,
        interceptorContext: {},
    });

    const marshal = (statusCode: number, responseBody: any): string => {
        let marshalledBody = responseBody;
        switch(statusCode) {
            case 200:
                marshalledBody = JSON.stringify(FormSchemaToJSON(marshalledBody));
                break;
            default:
                break;
        }

        return marshalledBody;
    };

    return {
        ...response,
        body: response.body ? marshal(response.statusCode, response.body) : '',
    };
};
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

export type UpdateStatus200OperationResponse = OperationResponse<200, FormMetadata>;
export type UpdateStatusOperationResponses = | UpdateStatus200OperationResponse ;

// Type that the handler function provided to the wrapper must conform to
export type UpdateStatusHandlerFunction = LambdaHandlerFunction<UpdateStatusRequestParameters, UpdateStatusRequestArrayParameters, UpdateStatusRequestBody, UpdateStatusOperationResponses>;
export type UpdateStatusChainedHandlerFunction = ChainedLambdaHandlerFunction<UpdateStatusRequestParameters, UpdateStatusRequestArrayParameters, UpdateStatusRequestBody, UpdateStatusOperationResponses>;

/**
 * Lambda handler wrapper to provide typed interface for the implementation of updateStatus
 */
export const updateStatusHandler = (
    firstHandler: UpdateStatusChainedHandlerFunction,
    ...remainingHandlers: UpdateStatusChainedHandlerFunction[]
): ApiGatewayLambdaHandler => async (event: any, context: any): Promise<any> => {
    const requestParameters = decodeRequestParameters({
        ...(event.pathParameters || {}),
        ...(event.queryStringParameters || {}),
    }) as unknown as UpdateStatusRequestParameters;

    const requestArrayParameters = decodeRequestParameters({
        ...(event.multiValueQueryStringParameters || {}),
    }) as unknown as UpdateStatusRequestArrayParameters;

    const demarshal = (bodyString: string): any => {
        let parsed = JSON.parse(bodyString);
        parsed = UpdateStatusInputFromJSON(parsed);
        return parsed;
    };
    const body = parseBody(event.body, demarshal, ['application/json',]) as UpdateStatusRequestBody;

    const chain = buildHandlerChain(firstHandler, ...remainingHandlers);
    const response = await chain.next({
        input: {
            requestParameters,
            requestArrayParameters,
            body,
        },
        event,
        context,
        interceptorContext: {},
    });

    const marshal = (statusCode: number, responseBody: any): string => {
        let marshalledBody = responseBody;
        switch(statusCode) {
            case 200:
                marshalledBody = JSON.stringify(FormMetadataToJSON(marshalledBody));
                break;
            default:
                break;
        }

        return marshalledBody;
    };

    return {
        ...response,
        body: response.body ? marshal(response.statusCode, response.body) : '',
    };
};
