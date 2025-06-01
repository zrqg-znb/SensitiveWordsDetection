from pydantic import BaseModel, Field

class TextCheckRequest(BaseModel):
    """
    文本检测请求模型
    """
    sentences: list[str] = Field(..., description="待检测的文本列表")