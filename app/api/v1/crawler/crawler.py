import urllib

from fastapi import APIRouter, Query, UploadFile, File
from app.controllers.crawler import crawler_controller
from tortoise.expressions import Q
import requests
from app.schemas.crawler import *
from app.schemas.base import Success, SuccessExtra, Fail

router = APIRouter()


@router.get('/list', summary="查看爬虫列表")
async def list_crawlers(
        page: int = Query(1, description="页码"),
        page_size: int = Query(10, description="每页数量"),
        search: str = Query(None, description="搜索关键词"),
        method: str = Query(None, description="请求方法"),
        user_id: int = Query(None, description="用户ID"),
):
    q = Q()
    if  user_id != 1:
        q &= Q(user_id=user_id)
    if search:
        q &= Q(Q(name__icontains=search) | Q(url__icontains=search))
    if method:
        q &= Q(method=method)
    total, crawler_objs = await crawler_controller.list(page=page, page_size=page_size, search=q, order=["-created_at"])
    data = [await obj.to_dict() for obj in crawler_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.post('/create', summary="创建爬虫")
async def create_crawler(
        crawler: CrawlerCreate,
):
    # print(crawler)
    await crawler_controller.create(obj_in=crawler)
    return Success(msg="爬虫创建成功")


@router.delete('/delete', summary="删除爬虫")
async def delete_crawler(
        crawler_id: int = Query(..., description="爬虫ID"),
):
    await crawler_controller.remove(id=crawler_id)
    return Success(msg="爬虫删除成功")


@router.post('/update', summary="更新爬虫")
async def update_crawler(
        crawler: CrawlerUpdate,
):
    await crawler_controller.update(id=crawler.id, boj_in=crawler)
    return Success(msg="爬虫更新成功")


@router.post('/do_crawler', summary="执行爬虫")
async def get_page(
        crawler_in: CrawlerCreate,
):
    res = await crawler_controller.do_crawler(crawler_in)
    if res:
        return Success(msg="爬虫执行成功")
    else:
        return Fail(msg="爬虫执行失败")


from app.schemas.text_check import TextCheckRequest
from app.schemas.base64_check import Base64CheckRequest


@router.post('/check_text', summary="文本/OCR检测")
async def check_text(
        request: TextCheckRequest
):
    report_url = await crawler_controller.check_text_content(request.sentences)
    if report_url:
        return Success(msg="检测成功", data={"report_url": report_url})
    else:
        return Fail(msg="检测失败")


@router.post('/get_base64', summary="上传base64获取ocr结果")
async def get_base64(
        request: Base64CheckRequest
):
    # 确保 base64 数据不包含前缀
    clean_base64 = request.base64_data.split(',')[-1] if ',' in request.base64_data else request.base64_data

    # URL 编码 Base64 字符串
    encoded_image = urllib.parse.quote_plus(clean_base64)

    payload = f'image={encoded_image}&detect_direction=false&detect_language=false&paragraph=false&probability=false'

    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=" + get_access_token()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))

    sentences = []
    if response.status_code == 200:
        data = response.json()
        if 'words_result' in data:
            for word_result in data['words_result']:
                sentences.append(word_result['words'])
            return Success(msg="检测成功", data={"sentences": sentences})
        else:
            return Fail(msg="检测失败")
    else:
        return Fail(msg="检测失败")



def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    API_KEY = "3mmTu2RNxD1g7Mb4VgXfgTZw"
    SECRET_KEY = "MnKjqMkdnBnRjfr0BICqQ6Bq3IRF0ARi"
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
