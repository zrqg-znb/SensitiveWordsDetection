from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `crawler` MODIFY COLUMN `user_id` INT   COMMENT '用户ID';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `crawler` MODIFY COLUMN `user_id` INT NOT NULL  COMMENT '用户ID';"""
