from typing import Annotated, Dict, List, Any
from fastapi import Depends
from app.common.provider.provider import provider_depp
from app.common.helper_function import logger_depp
from .model import ComputeInstance, ComputeMetric
from datetime import date

class ComputeService:
    def __init__(self, *, logger: logger_depp, provider: provider_depp):
        self._logger = logger
        self._provider = provider

    def list(self) -> List[ComputeInstance] | None:
        self._logger.info('ComputeService list')
        compute_list = self._provider.get_compute_list()
        if len(compute_list):
            compute_list_model = [ComputeInstance(**v) for v in compute_list]
            return compute_list_model
        else:
            return None

    def metric(self, start_date:date, end_date: date) -> ComputeMetric | None:
        self._logger.info('ComputeService list')
        compute_list = self._provider.get_compute_list()
        if len(compute_list):
            compute_list_model = [ComputeInstance(**v) for v in compute_list]
            compute_cost = self._provider.get_compute_cost(start_date=start_date, end_date=end_date)
            return ComputeMetric(instances=compute_list_model, total_cost=compute_cost)
        else:
            return None

compute_depp = Annotated[ComputeService, Depends(ComputeService)]