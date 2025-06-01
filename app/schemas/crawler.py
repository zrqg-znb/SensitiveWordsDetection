from pydantic import BaseModel, Field

from app.models.enums import MethodType


class BaseCrawler(BaseModel):
    """
    爬虫基类
    """
    url: str = Field(..., description="爬虫地址")
    headers: dict = Field(..., description="爬虫请求头")
    params: dict = Field(..., description="爬虫请求参数")
    method: str = Field(..., description="爬虫请求方法")
    # 爬虫的请求结果
    result_url: str = Field(..., description="爬虫请求结果报告的url")
    user_id: int = Field(..., description="爬虫所属用户id")


class CrawlerCreate(BaseCrawler): ...


class CrawlerUpdate(BaseCrawler):
    id: int
