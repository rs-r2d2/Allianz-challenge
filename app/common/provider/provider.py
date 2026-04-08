from typing import Annotated
from fastapi import Depends
from .provider_base import ProviderBase
from .aws_provider import AWSProvider
from app.common.helper_function import logger_depp, session_depp

def get_provider(logger: logger_depp, boto3: session_depp) -> ProviderBase:
    return AWSProvider(logger = logger, boto3 = boto3)

provider_depp = Annotated[AWSProvider, Depends(get_provider)]