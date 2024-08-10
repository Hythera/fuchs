CREATE TABLE IF NOT EXISTS `level_users` (
    `client_id` BIGINT NOT NULL,
    `xp` BIGINT NOT NULL DEFAULT 0,
    `messages` BIGINT NOT NULL DEFAULT 0,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`client_id`)
);
CREATE TABLE IF NOT EXISTS `economy_users` (
    `client_id` BIGINT NOT NULL,
    `coins` BIGINT NOT NULL DEFAULT 0,
    `multiplier` FLOAT NOT NULL DEFAULT 1,
    `job` VARCHAR(255) NOT NULL DEFAULT 'None', 
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`client_id`)
)