from fastapi import APIRouter

from .sensitive_words import router

sensitive_word_router = APIRouter()
sensitive_word_router.include_router(router, tags=['敏感词模块'])

__all__ = ['sensitive_word_router']
