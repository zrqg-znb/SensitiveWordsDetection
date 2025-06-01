from app.core.crud import CRUDBase
from app.schemas.sensitive_word import SensitiveWordCreate, SensitiveWordUpdate
from app.models.admin import SensitiveWord


class SensitiveWordController(CRUDBase[SensitiveWord, SensitiveWordCreate, SensitiveWordUpdate]):
    def __init__(self):
        super().__init__(model=SensitiveWord)

    async def toggle_sensitive_word_status(self, word_id: int):
        word = await self.model.get(id=word_id)
        word.is_active = not word.is_active
        await word.save()

    # 获取所有的数据
    async def get_sensitive_words(self):
        query = self.model.all()
        query = query.filter(is_active=True)
        total, sensitive_words = await self.list(query)
        return total, sensitive_words


sensitive_word_controller = SensitiveWordController()
