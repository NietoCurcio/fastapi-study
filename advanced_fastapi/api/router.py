from fastapi import APIRouter

from advanced_fastapi.api.routes import (
    root_router,
    gzip_router,
)

api_router = APIRouter()

api_router.include_router(root_router, prefix='/api', tags=['api'])
api_router.include_router(gzip_router, prefix='/gzip', tags=['gzip'])
