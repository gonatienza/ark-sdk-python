from typing import Optional

from pydantic import Field

from ark_sdk_python.models import ArkModel


class ArkSIASSOGetShortLivedRDPFile(ArkModel):
    allow_caching: bool = Field(description='Allow short lived token caching', default=True)
    folder: str = Field(description='Output folder to write the rdp file to')
    target_address: str = Field(description='Address of the Windows target machine')
    target_domain: Optional[str] = Field(default=None, description='Domain of the Windows target machine')
    target_user: Optional[str] = Field(default=None, description='Name of the target user to connect with')
    elevated_privileges: Optional[bool] = Field(default=None, description='whether to run session with elevated privileges')
