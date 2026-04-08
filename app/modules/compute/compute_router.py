from fastapi import APIRouter
from datetime import date
from .compute_service import compute_depp
from .model import ComputeMetric

router = APIRouter()

@router.get("/compute")
def compute(compute_service: compute_depp):
    return compute_service.list()

@router.get("/compute/metrics")
def compute(compute_service: compute_depp, start_date: str, end_date: str) -> ComputeMetric | None:
    return compute_service.metric(start_date=date.fromisoformat(start_date), end_date=date.fromisoformat(end_date))

