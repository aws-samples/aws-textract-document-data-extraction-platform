from aws_api_python_runtime.paths.schemas_schema_id.get import ApiForget
from aws_api_python_runtime.paths.schemas_schema_id.put import ApiForput
from aws_api_python_runtime.paths.schemas_schema_id.delete import ApiFordelete


class SchemasSchemaId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
