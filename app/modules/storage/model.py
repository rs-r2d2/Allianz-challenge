from pydantic import BaseModel
from typing import List

class StorageInstance(BaseModel):
    bucket_name: str
    instance_type: str
    state: str
    tax: str

class StorageMetric(BaseModel):
    instances: List[StorageInstance]
    total_cost: float
