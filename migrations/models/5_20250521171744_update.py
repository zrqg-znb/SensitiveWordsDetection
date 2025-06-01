from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `crawler` DROP INDEX `idx_crawler_user_id_6179c9`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `crawler` ADD INDEX `idx_crawler_user_id_6179c9` (`user_id`);"""
