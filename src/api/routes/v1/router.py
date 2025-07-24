from fastapi import APIRouter

from src.api.routes.v1.endpoints import eval

api_router = APIRouter()
api_router.include_router(eval.router, prefix="/eval", tags=["eval"])
