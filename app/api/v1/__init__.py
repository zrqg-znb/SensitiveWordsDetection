from fastapi import APIRouter

from app.core.dependency import DependPermisson

from .apis import apis_router
from .auditlog import auditlog_router
from .base import base_router
from .depts import depts_router
from .menus import menus_router
from .roles import roles_router
from .users import users_router
from .sen_words import sensitive_word_router
from .crawler import crawler_router
v1_router = APIRouter()

v1_router.include_router(base_router, prefix="/base")
v1_router.include_router(users_router, prefix="/user")
v1_router.include_router(roles_router, prefix="/role", dependencies=[DependPermisson])
v1_router.include_router(menus_router, prefix="/menu", dependencies=[DependPermisson])
v1_router.include_router(apis_router, prefix="/api", dependencies=[DependPermisson])
v1_router.include_router(depts_router, prefix="/dept", dependencies=[DependPermisson])
v1_router.include_router(auditlog_router, prefix="/auditlog", dependencies=[DependPermisson])
v1_router.include_router(sensitive_word_router, prefix="/sen_words", dependencies=[DependPermisson])
v1_router.include_router(crawler_router, prefix="/crawler", dependencies=[DependPermisson])