-- Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn/Python-Discord-Bot-Template/blob/main/database/schema.sql

CREATE TABLE IF NOT EXISTS `warns` (
  `id` int(11) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `moderator_id` varchar(20) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `tags` (
  `tid` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` varchar(255) NOT NULL,
  `content` TEXT NOT NULL,
  `author` varchar(20) NOT NULL,
  `guild` varchar(20),
  `used` INTEGER DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `tag_buttons` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `tag_id` INTEGER NOT NULL,
  `label` varchar(80) NOT NULL,
  `url` TEXT NOT NULL,
  `emoji` varchar(100),
  FOREIGN KEY (tag_id) REFERENCES tags(tid) ON DELETE CASCADE
);