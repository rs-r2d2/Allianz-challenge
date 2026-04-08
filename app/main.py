from fastapi import FastAPI

from app.modules.compute import compute_router
from app.modules.storage import storage_router

app = FastAPI()

app.include_router(compute_router.router)
app.include_router(storage_router.router)

@app.get("/")
async def root():
    return {"message": "health endpoint"}