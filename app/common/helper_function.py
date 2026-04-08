import logging
from typing import Annotated
from fastapi import Depends
import boto3
import os

def get_logger() -> logging.Logger:
    app_logger = logging.getLogger('app')
    return app_logger

logger_depp = Annotated[logging.Logger, Depends(get_logger)]


def get_session() -> boto3.Session:
    session = boto3.Session(profile_name=os.environ.get('profile'))
    return session

session_depp = Annotated[boto3.Session, Depends(get_session)]
