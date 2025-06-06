from pydantic import Field

from ark_sdk_python.models.services.sia.db.ark_sia_db_base_execution import ArkSIADBBaseExecution


class ArkSIADBPsqlExecution(ArkSIADBBaseExecution):
    psql_path: str = Field(description='Path to the psql executable', default='psql')
