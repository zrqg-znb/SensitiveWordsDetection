from pydantic import BaseModel, Field

class Base64CheckRequest(BaseModel):
    """
    Base64图片检测请求模型
    """
    base64_data: str = Field(..., description="Base64编码的图片数据")