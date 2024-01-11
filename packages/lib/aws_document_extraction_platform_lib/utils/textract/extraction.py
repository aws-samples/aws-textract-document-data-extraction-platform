#
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT-0
#
from dataclasses import dataclass
import math
import statistics
import dateutil
from typing import Dict, List, Any, Optional, TypedDict

from aws_document_extraction_platform_api_python_runtime.model.form_json_schema import FormJSONSchema
from trp import Document, Field, Cell, Table, BaseBlock
from trp.trp2 import TDocument, TDocumentSchema, TBlock
from trp.t_pipeline import order_blocks_by_geo
from aws_document_extraction_platform_lib.utils.logger import get_logger

log = get_logger(__name__)


@dataclass
class DocumentField:
    field: Field
    page_index: int


@dataclass
class DocumentTable:
    table: Table
    page_index: int


@dataclass
class DocumentCell:
    cell: Cell
    page_index: int


@dataclass
class DocumentQueryAnswer:
    value: str
    page_index: int
    block: BaseBlock


class ExtractionMethods:
    FORM = "FORM"
    TABLE = "TABLE"
    QUERY = "QUERY"


class StatefulDocumentLookupData:
    """
    Class to manage stateful lookup of fields in documents. When fields are successfully looked up, they are removed,
    thus ensuring that duplicate form keys do not always return the value for the first occurrence in the document.
    """

    document: Document
    document_trp2: TDocument
    document_fields: Dict[str, List[DocumentField]]
    lower_key_to_originals: Dict[str, List[str]]
    tables: List[DocumentTable]

    # Map of query alias to a list of answers found in the document, ordered by page number
    query_answers: Dict[str, List[DocumentQueryAnswer]]

    current_block_index: int

    def __init__(self, textract_result: Dict):
        """
        Preprocess the document for fast stateful lookup of fields
        """
        self.document = Document(textract_result)
        self.document_trp2 = order_blocks_by_geo(
            TDocumentSchema().load(textract_result)
        )
        self.document_fields = {}
        self.lower_key_to_originals = {}
        self.tables = []
        self.query_answers = {}
        self.current_block_index = 0
        self.ordered_blocks_by_geo = {}

        # Preprocess fields and tables
        for i in range(0, len(self.document.pages)):
            page = self.document.pages[i]
            for field in page.form.fields:
                if field.key is not None and field.key.text is not None:
                    self.add_field(DocumentField(field=field, page_index=i))
            self.tables += [DocumentTable(table, i) for table in page.tables]

        # Preprocess query answers
        for i in range(0, len(self.document_trp2.pages)):
            page = self.document_trp2.pages[i]
            for query in self.document_trp2.queries(page):
                if query.query.alias not in self.query_answers:
                    self.query_answers[query.query.alias] = []
                for answer in self.document_trp2.get_answers_for_query(query):
                    self.query_answers[query.query.alias].append(
                        DocumentQueryAnswer(
                            value=answer.text, page_index=i, block=_to_block(answer)
                        )
                    )
        self.ordered_blocks_by_geo = {
            self.document_trp2.blocks[i].id: i
            for i in range(0, len(self.document_trp2.blocks))
        }

    def add_field(self, field: DocumentField):
        """
        Add a field to the document lookup data
        """
        field_key = field.field.key.text
        if field_key not in self.document_fields:
            self.document_fields[field_key] = []
        self.document_fields[field_key].append(field)

        lower_key = field_key.lower()
        if lower_key not in self.lower_key_to_originals:
            self.lower_key_to_originals[lower_key] = []
        self.lower_key_to_originals[lower_key].append(field_key)

    def _find_closest_block_before_current_index(self, blocks, get_id):
        closest_distance = None
        closest_block = None
        for block in blocks:
            distance = (
                self.ordered_blocks_by_geo[get_id(block)] - self.current_block_index
            )
            if distance <= 0:
                if closest_distance is None or distance > closest_distance:
                    closest_distance = distance
                    closest_block = block
        return closest_block

    def _get(self, key: str) -> Optional[DocumentField]:
        """
        Retrieve the first field in the document that matches the given key, "consuming" the field if found
        """
        if key in self.document_fields:
            for idx, field in enumerate(self.document_fields[key]):
                if field is not None:
                    # Find the closest form field after our current position
                    if (
                        self.ordered_blocks_by_geo[field.field.id]
                        > self.current_block_index
                    ):
                        doc_field = self.document_fields[key][idx]
                        self.document_fields[key].pop(idx)
                        return doc_field

            # get closest field with smallest negative distance from current block index
            closest_document_field = self._find_closest_block_before_current_index(
                self.document_fields[key], lambda f: f.field.id
            )

            if closest_document_field is not None:
                delete_index = self.document_fields[key].index(closest_document_field)
                self.document_fields[key].pop(delete_index)
                return closest_document_field
        # No more occurrences of the field exist, or it doesn't exist in the document
        return None

    def lookup_field(self, key: str) -> Optional[DocumentField]:
        """
        Look up a form field in the document
        :param key: the form key to look for
        :return: a field from the document if found
        """
        # Try an exact match
        field = self._get(key)

        if field is not None:
            self.current_block_index = self.ordered_blocks_by_geo[field.field.id]
            return field

        # Try a case insensitive match
        if key in self.lower_key_to_originals:
            for original_key in self.lower_key_to_originals[key]:
                field = self._get(original_key)
                if field is not None:
                    self.current_block_index = self.ordered_blocks_by_geo[
                        field.field.id
                    ]
                    return field
        # Could not be found
        return None

    def lookup_table_cell(self, schema: FormJSONSchema) -> Optional[DocumentCell]:
        """
        Look up a table cell at the position defined in the schema (if present)
        :param schema: the schema defining the table, row and column position
        :return: the table cell (if present)
        """
        if not (
            "extractionMetadata" in schema
            and "tablePosition" in schema["extractionMetadata"]
            and "rowPosition" in schema["extractionMetadata"]
            and "columnPosition" in schema["extractionMetadata"]
        ):
            return None

        # Positions in the schema are 1-indexed
        t = int(schema["extractionMetadata"]["tablePosition"] - 1)
        r = int(schema["extractionMetadata"]["rowPosition"] - 1)
        c = int(schema["extractionMetadata"]["columnPosition"] - 1)
        if (
            0 <= t < len(self.tables)
            and 0 <= r < len(self.tables[t].table.rows)
            and 0 <= c < len(self.tables[t].table.rows[r].cells)
        ):
            self.current_block_index = self.ordered_blocks_by_geo[
                self.tables[t].table.rows[r].cells[c].id
            ]
            return DocumentCell(
                cell=self.tables[t].table.rows[r].cells[c],
                page_index=self.tables[t].page_index,
            )

        return None

    def lookup_query_answer(self, alias: str) -> Optional[DocumentQueryAnswer]:
        """
        Look up a query answer from the textract document response.
        :param alias: the query alias (the property key)
        :return: the query answer if available
        """
        if alias in self.query_answers:
            answers = self.query_answers[alias]
            # Return the first answer on/after the current block index if possible
            for answer in answers:
                if (
                    self.ordered_blocks_by_geo[answer.block.id]
                    > self.current_block_index
                ):
                    self.current_block_index = self.ordered_blocks_by_geo[
                        answer.block.id
                    ]
                    return answer
                # else return the answer with closest negative distance
            closest_answer = self._find_closest_block_before_current_index(
                answers, lambda a: a.block.id
            )
            if closest_answer is not None:
                self.current_block_index = self.ordered_blocks_by_geo[
                    closest_answer.block.id
                ]
                return closest_answer
        return None


class BoundingBox(TypedDict):
    top: float
    left: float
    width: float
    height: float


class ExtractedFormValueMetadata(TypedDict):
    confidence: float
    box: BoundingBox
    page: int
    originalValue: str
    extractionMethod: str


@dataclass
class ExtractedFormData:
    # The data extracted from a document according to the schema.
    # This would be the value in a form field for a simple string, or a dictionary for an object type, etc.
    data: Any
    # The metadata, including confidence of data extracted from the document. This has the same shape as the above,
    # but leaf values are ExtractedFormValueMetadata objects
    metadata: Any
    # Whether or not any field was found in the extracted form data, useful for searching for an unknown number
    # of items in an array schema
    found_any_field: bool
    # The average confidence value for the extracted data
    average_confidence: float


def _to_block(block: TBlock) -> BaseBlock:
    """
    Convert a trp2 block to a trp block
    """
    return BaseBlock(
        {
            "Id": block.id,
            "Confidence": block.confidence,
            "Geometry": {
                "BoundingBox": {
                    "Width": block.geometry.bounding_box.width,
                    "Height": block.geometry.bounding_box.height,
                    "Top": block.geometry.bounding_box.top,
                    "Left": block.geometry.bounding_box.left,
                },
                "Polygon": [
                    {
                        "X": point.x,
                        "Y": point.y,
                    }
                    for point in block.geometry.polygon
                ],
            },
            "Text": block.text,
            "Custom": block.custom,
            "TextType": block.text_type,
        },
        None,
    )


def ordered_object_schema_property_keys(schema: FormJSONSchema) -> List[str]:
    """
    Return the object schema's property keys in order (determined by the 'order' attribute if present). Assumes given
    schema is an object schema.
    """

    def _get_order(property_key: str) -> float:
        property = schema["properties"][property_key]
        return float(property["order"]) if "order" in property else math.inf

    return sorted((schema["properties"] or {}).keys(), key=_get_order)


def get_form_keys_from_schema(schema: FormJSONSchema) -> List[str]:
    """
    Return the key to look up in a form from the schema for a primitive value
    """
    keys = []
    if (
        "extractionMetadata" in schema
        and "formKey" in schema["extractionMetadata"]
        and schema["extractionMetadata"]["formKey"] is not None
    ):
        keys.append(schema["extractionMetadata"]["formKey"])
    if "title" in schema and schema["title"] is not None:
        keys.append(schema["title"])
    return keys


def _build_metadata(
    block: BaseBlock, page_index: int, original_value: str, extraction_method: str
) -> ExtractedFormValueMetadata:
    """
    Return the metadata object for a textract block
    """
    return {
        "confidence": block.confidence,
        "box": {
            "top": block.geometry.boundingBox.top,
            "left": block.geometry.boundingBox.left,
            "width": block.geometry.boundingBox.width,
            "height": block.geometry.boundingBox.height,
        },
        "page": page_index,
        "originalValue": original_value,
        "extractionMethod": extraction_method,
    }


def _build_field_metadata(
    field: Field, page_index: int, extraction_method: str
) -> ExtractedFormValueMetadata:
    """
    Build the metadata object from a form field.
    """
    # Prefer more "specific" metadata for the field value if present, otherwise use the entire field
    block = field.value if field.value is not None else field
    original_value = field.value.text if field.value is not None else None
    return _build_metadata(block, page_index, original_value, extraction_method)


def _coerce_value(value: str, schema: FormJSONSchema):
    """
    Return the value in the type specified by the schema (where possible)
    """
    try:
        if schema["typeOf"] == "integer":
            return int(value.replace(",", ""))
        elif schema["typeOf"] == "number":
            return float(value.replace(",", ""))
        elif schema["typeOf"] == "boolean":
            # TODO: May wish to consider other falsy values where we expect a boolean value from a form
            return value.lower() not in {"no", "false", ""}
        else:
            # Schema type is 'string'
            if "formatType" in schema:
                # TODO: May wish to consider supporting full range of built in formats https://json-schema.org/understanding-json-schema/reference/string.html#built-in-formats
                if schema["formatType"] in {"date", "date-time"}:
                    # Python's date parser handles lots of formats, but may wish to extend if there are other common formats not supported
                    return dateutil.parser.parse(value).isoformat()
            return value
    except Exception as e:
        log.exception(e)
        log.warning(
            "Unable to parse value {} into type {}, will return as raw string".format(
                value, schema["typeOf"]
            )
        )
        return value


def _coerce_field_value(field: Field, schema: FormJSONSchema):
    """
    Return the field value in the type specified by the schema
    """
    # Empty fields will have value as None
    field_value_text = (
        field.value.text
        if field.value is not None and field.value.text is not None
        else ""
    )
    return _coerce_value(field_value_text, schema)


def _extract_schema_fields(
    document_data: StatefulDocumentLookupData,
    schema: FormJSONSchema,
    property_path: str = "",
) -> ExtractedFormData:
    """
    Extract the fields defined in the schema from the document lookup data
    """
    if schema["typeOf"] == "object":
        object_data: Dict = {}
        object_metadata: Dict = {}
        found_any_field = False
        object_confidences: List[float] = []
        for property_key in ordered_object_schema_property_keys(schema):
            extracted_data = _extract_schema_fields(
                document_data,
                schema["properties"][property_key],
                property_path + ("" if len(property_path) == 0 else ".") + property_key,
            )
            object_data[property_key] = extracted_data.data
            object_metadata[property_key] = extracted_data.metadata
            found_any_field = found_any_field or extracted_data.found_any_field
            object_confidences.append(extracted_data.average_confidence)
        return ExtractedFormData(
            data=object_data,
            metadata=object_metadata,
            found_any_field=found_any_field,
            average_confidence=statistics.mean(object_confidences)
            if len(object_confidences) > 0
            else 0,
        )

    elif schema["typeOf"] == "array":
        # TODO: May wish to consider enhancing this algorithm for arrays, perhaps also taking into account the min/max
        # length properties if set
        # For now we keep extracting until we can't find anything from the array's subschema in the document
        found_any_fields = True

        list_data: List[Any] = []
        list_metadata: List[Any] = []
        list_confidences: List[float] = []

        i = 0
        while found_any_fields:
            extracted_data = _extract_schema_fields(
                document_data, schema.items, "{}[{}]".format(property_path, i)
            )
            list_confidences.append(extracted_data.average_confidence)
            found_any_fields = extracted_data.found_any_field
            if found_any_fields:
                list_data.append(extracted_data.data)
                list_metadata.append(extracted_data.metadata)
            i += 1

        return ExtractedFormData(
            data=list_data,
            metadata=list_metadata,
            found_any_field=len(list_data) > 0,
            average_confidence=statistics.mean(list_confidences)
            if len(list_confidences) > 0
            else 0,
        )

    # Primitive type (string, int etc)

    # Try looking up from a query first if present
    query_answer = document_data.lookup_query_answer(property_path)
    if query_answer is not None:
        metadata = _build_metadata(
            query_answer.block,
            query_answer.page_index,
            query_answer.value,
            ExtractionMethods.QUERY,
        )
        return ExtractedFormData(
            data=_coerce_value(query_answer.value, schema),
            metadata=metadata,
            found_any_field=True,
            average_confidence=metadata["confidence"],
        )

    # Next, try looking up with textract forms
    keys = get_form_keys_from_schema(schema)
    for key in keys:
        field = document_data.lookup_field(key)
        if field is not None:
            metadata = _build_field_metadata(
                field.field, field.page_index, ExtractionMethods.FORM
            )
            return ExtractedFormData(
                data=_coerce_field_value(field.field, schema),
                metadata=metadata,
                found_any_field=True,
                average_confidence=metadata["confidence"],
            )

    # We couldn't find the value with queries or forms, try via table position
    cell = document_data.lookup_table_cell(schema)
    if cell is not None:
        metadata = _build_metadata(
            cell.cell, cell.page_index, cell.cell.text, ExtractionMethods.TABLE
        )
        return ExtractedFormData(
            data=_coerce_value(cell.cell.text or "", schema),
            metadata=metadata,
            found_any_field=True,
            average_confidence=metadata["confidence"],
        )

    return ExtractedFormData(
        data=None, metadata=None, found_any_field=False, average_confidence=0
    )


def extract_schema_fields_from_document(
    textract_result: Dict, schema: FormJSONSchema
) -> ExtractedFormData:
    """
    Given a textract document result and a schema, extract data from the document that conforms to the schema
    """
    document_data = StatefulDocumentLookupData(textract_result)
    return _extract_schema_fields(document_data, schema)
