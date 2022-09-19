from api_python_client.paths.schemas_schema_id.get import ApiForget
from api_python_client.paths.schemas_schema_id.put import ApiForput
from api_python_client.paths.schemas_schema_id.delete import ApiFordelete


class SchemasSchemaId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
