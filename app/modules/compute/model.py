from pydantic import BaseModel
from typing import List

class ComputeInstance(BaseModel):
    instance_id: str
    instance_type: str
    state: str
    tax: str

class ComputeMetric(BaseModel):
    instances: List[ComputeInstance]
    total_cost: float
