from fastapi import APIRouter
from .crawler import router

crawler_router = APIRouter()
crawler_router.include_router(router, tags=["爬虫"])

__all__ = ['crawler_router']