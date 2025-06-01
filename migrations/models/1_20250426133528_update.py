from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `sensitive_word` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `word` VARCHAR(255) NOT NULL  COMMENT '敏感词',
    `category` VARCHAR(255) NOT NULL  COMMENT '分类',
    `level` INT NOT NULL  COMMENT '敏感级别' DEFAULT 1,
    `is_active` BOOL NOT NULL  COMMENT '是否启用' DEFAULT 1,
    `remark` VARCHAR(500)   COMMENT '备注',
    KEY `idx_sensitive_w_created_001901` (`created_at`),
    KEY `idx_sensitive_w_updated_ff92e5` (`updated_at`),
    KEY `idx_sensitive_w_word_11f4b7` (`word`),
    KEY `idx_sensitive_w_categor_734a19` (`category`),
    KEY `idx_sensitive_w_level_039ab6` (`level`),
    KEY `idx_sensitive_w_is_acti_a1b1ba` (`is_active`)
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `sensitive_word`;"""
