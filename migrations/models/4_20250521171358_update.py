from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `crawler` ADD `user_id` INT NOT NULL  COMMENT '用户ID';
        ALTER TABLE `crawler` ADD INDEX `idx_crawler_user_id_6179c9` (`user_id`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `crawler` DROP INDEX `idx_crawler_user_id_6179c9`;
        ALTER TABLE `crawler` DROP COLUMN `user_id`;"""
