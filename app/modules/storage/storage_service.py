from typing import Annotated, Dict, List, Any
from fastapi import Depends
from app.common.provider.provider import provider_depp
from app.common.helper_function import logger_depp
from .model import StorageInstance, StorageMetric
from datetime import date

class StorageService:
    def __init__(self, *, logger: logger_depp, provider: provider_depp):
        self._logger = logger
        self._provider = provider

    def list(self) -> List[StorageInstance] | None:
        self._logger.info('StorageService list')
        compute_list = self._provider.get_storage_list()
        if len(compute_list):
            compute_list_model = [StorageInstance(**v) for v in compute_list]
            return compute_list_model
        else:
            return None

    def metric(self, start_date: date, end_date: date) -> StorageMetric | None:
        self._logger.info('StorageService list')
        compute_list = self._provider.get_storage_list()
        if len(compute_list):
            list_model = [StorageInstance(**v) for v in compute_list]
            compute_cost = self._provider.get_storage_cost(start_date=start_date, end_date=end_date)
            return StorageMetric(instances=list_model, total_cost=compute_cost)
        else:
            return None

storage_depp = Annotated[StorageService, Depends(StorageService)]