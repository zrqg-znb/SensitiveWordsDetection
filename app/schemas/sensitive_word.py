from pydantic import BaseModel, Field


class BaseSensitiveWord(BaseModel):
    category: str = Field(..., description="敏感词分类", max_length=50)
    level: int = Field(1, description="敏感级别(1-3)", ge=1, le=3)
    word: str = Field(..., description="敏感词内容", max_length=100)
    is_active: bool = Field(True, description="是否启用")


class SensitiveWordCreate(BaseSensitiveWord): ...


class SensitiveWordUpdate(BaseSensitiveWord):
    id: int