from pydantic import ConfigDict, Field, StringConstraints
from typing_extensions import Annotated

from ark_sdk_python.models import ArkCamelizedModel


class ArkSMSessionsFilter(ArkCamelizedModel):
    search: Annotated[str, StringConstraints(max_length=4096)] = Field(
        description='Free text query to search sessions by. For example: "startTime GE 2023-11-18T06:53:30Z AND status IN Failed,Ended AND endReason STARTSWITH Err008"'
    )
    model_config = ConfigDict(
        json_schema_extra={
            'examples': [
                {
                    'search': 'duration LE 01:00:00',
                },
                {
                    'search': 'startTime GE 2023-11-18T06:53:30Z',
                },
                {
                    'search': 'status IN Failed,Ended AND endReason STARTSWITH Err008',
                },
                {
                    'search': 'command STARTSWITH ls',
                },
                {
                    'search': 'protocol IN SSH,RDP',
                },
            ]
        }
    )
