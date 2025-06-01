from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `crawler` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `url` VARCHAR(255) NOT NULL  COMMENT 'URL地址',
    `method` VARCHAR(6) NOT NULL  COMMENT '请求方法',
    `headers` JSON   COMMENT '请求头',
    `params` JSON   COMMENT '请求参数',
    `result_url` VARCHAR(500) NOT NULL  COMMENT '结果报告URL',
    KEY `idx_crawler_created_00f0fa` (`created_at`),
    KEY `idx_crawler_updated_2adf38` (`updated_at`),
    KEY `idx_crawler_url_e1ea0e` (`url`),
    KEY `idx_crawler_method_066bf6` (`method`),
    KEY `idx_crawler_result__6710cc` (`result_url`)
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `crawler`;"""
