--
-- This script inicializes new MySQL database for Simplyletters
--


--
-- TABLES
--


CREATE TABLE newsletters (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    user_group INT,
    html_render TEXT, 
    slug TEXT,
    status BOOLEAN DEFAULT '0', 
    sent TINYTEXT DEFAULT null,
    created TINYTEXT,
    created_by TEXT);


CREATE TABLE newsletters_content (
    id INT,
    template INT,
    color_main TINYTEXT,
    color_accent TINYTEXT,
    color_text TINYTEXT,
    title TINYTEXT,
    perex TEXT,
    perex_header TEXT);


CREATE TABLE newsletters_paragraphs (
    id INT,
    paragraph_id INT AUTO_INCREMENT PRIMARY KEY,
    header TEXT,
    text TEXT,
    image TEXT);


CREATE TABLE newsletters_config (
    logo TEXT,
    footer TEXT);


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    email VARCHAR(255) NOT NULL,
    firstname TEXT,
    surname TEXT,
    active BOOLEAN DEFAULT '1',
    since TINYTEXT,
    
    UNIQUE (email));


CREATE TABLE user_groups (
    id INT AUTO_INCREMENT  PRIMARY KEY,
    name TEXT,
    description TEXT);


CREATE TABLE users_in_groups (
    group_id INT,
    user_id INT);


CREATE TABLE email_credentials (
    email TINYTEXT,
    password TINYTEXT,
    smtp_server TINYTEXT);


CREATE TABLE admins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username TINYTEXT,
    hash TEXT,
    level INT
);


CREATE TABLE config (
    company_name TINYTEXT,
    description TEXT
);

CREATE TABLE connected_apps (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name TEXT,
    api_key TINYTEXT,
    user_group INT,
    description TINYTEXT
);

COMMIT;



--
-- Initial data
--

INSERT INTO
newsletters_config
(
    logo,
    footer
)
VALUES
(
    'This is a logo!',
    'This is a footer!'
);

COMMIT;

