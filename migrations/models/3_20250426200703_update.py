from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `crawler` MODIFY COLUMN `method` VARCHAR(10) NOT NULL  COMMENT '请求方法';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `crawler` MODIFY COLUMN `method` VARCHAR(6) NOT NULL  COMMENT '请求方法';"""
