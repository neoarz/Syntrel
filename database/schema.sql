-- Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn/Python-Discord-Bot-Template/blob/main/database/schema.sql
-- Used by neoarz

CREATE TABLE IF NOT EXISTS `warns` (
  `id` int(11) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `moderator_id` varchar(20) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);