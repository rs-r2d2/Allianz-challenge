from fastapi import APIRouter
from datetime import date
from typing import List
from .storage_service import storage_depp
from .model import StorageInstance, StorageMetric

router = APIRouter()

@router.get("/storage")
def storage_list(storage_service: storage_depp) -> List[StorageInstance] | None:
    return storage_service.list()

@router.get("/storage/metrics")
def storage_metric(storage_service: storage_depp, start_date: str, end_date: str) -> StorageMetric | None:
    return storage_service.metric(start_date=date.fromisoformat(start_date), end_date=date.fromisoformat(end_date))