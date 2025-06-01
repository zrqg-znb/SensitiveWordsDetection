from fastapi import APIRouter, Query
from app.controllers.sensitive_word import sensitive_word_controller
from tortoise.expressions import Q

from app.schemas.sensitive_word import *
from app.schemas.base import Fail, Success, SuccessExtra

router = APIRouter()


@router.get("/list", summary="查看敏感词列表")
async def lisr_sen_words(
        page: int = Query(1, description="页码"),
        page_size: int = Query(10, description="每页数量"),
        category: str = Query(None, description="分类"),
        is_active: bool = Query(None, description="是否启用"),
        word: str = Query(None, description="敏感词关键字"),
        level: str = Query(None, description="敏感级别"),
):
    q = Q()
    # 按照创建时间倒序
    # q &= Q(order_by="-created_at")
    if category:
        q &= Q(category__contains=category)
    if is_active is not None:
        q &= Q(is_active=is_active)
    if word:
        q &= Q(word__contains=word)
    if level:
        q &= Q(level=int(level))
    total, word_objs = await sensitive_word_controller.list(
        page=page, page_size=page_size, search=q
    )
    data = [await obj.to_dict() for obj in word_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="查看敏感词")
async def get_sensitive_word(
        word_id: int = Query(..., description="敏感词ID"),
):
    word_obj = await sensitive_word_controller.get(id=word_id)
    word_dict = await word_obj.to_dict()
    return Success(data=word_dict)


@router.post("/create", summary="创建敏感词")
async def create_sensitive_word(
        word: SensitiveWordCreate,
):
    await sensitive_word_controller.create(obj_in=word)
    return Success(msg="敏感词创建成功")


@router.delete("/delete", summary="删除敏感词")
async def delete_sensitive_word(
        word_id: int = Query(..., description="敏感词ID"),
):
    await sensitive_word_controller.remove(id=word_id)
    return Success(msg="敏感词删除成功")


@router.post("/update", summary="更新敏感词")
async def update_sensitive_word(
        word_in: SensitiveWordUpdate,
):
    await sensitive_word_controller.update(id=word_in.id, obj_in=word_in)
    return Success(msg="敏感词更新成功")


@router.post("/toggle", summary="切换敏感词状态")
async def toggle_sensitive_word_status(
        word_id: int = Query(..., description="敏感词ID"),
):
    await sensitive_word_controller.toggle_sensitive_word_status(word_id=word_id)
    return Success(msg="敏感词状态切换成功")
