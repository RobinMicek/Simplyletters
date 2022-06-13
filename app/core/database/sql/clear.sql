--
-- This script clears used MySQL database for Simplyletters
--


-- Drop all tables
DROP TABLE IF EXISTS 
newsletters, newsletters_config, newsletters_content, newsletters_paragraphs, 
users, user_groups, users_in_groups, email_credentials,
admins, config, connected_apps
