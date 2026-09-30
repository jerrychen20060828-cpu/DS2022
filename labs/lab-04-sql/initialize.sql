-- Recreate the related tables so this script can be run more than once.
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    created_at DATETIME NOT NULL
);

CREATE TABLE posts (
    post_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    body TEXT NOT NULL,
    published_at DATETIME,
    CONSTRAINT fk_posts_users
        FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO users (user_id, username, email, created_at)
VALUES (1, 'alex_rivera', 'alex.rivera@example.com', '2026-09-01 09:15:00');
INSERT INTO users (user_id, username, email, created_at)
VALUES (2, 'blair_chen', 'blair.chen@example.com', '2026-09-02 10:30:00');
INSERT INTO users (user_id, username, email, created_at)
VALUES (3, 'casey_morgan', 'casey.morgan@example.com', '2026-09-03 11:45:00');
INSERT INTO users (user_id, username, email, created_at)
VALUES (4, 'devon_patel', 'devon.patel@example.com', '2026-09-04 13:00:00');
INSERT INTO users (user_id, username, email, created_at)
VALUES (5, 'ellis_johnson', 'ellis.johnson@example.com', '2026-09-05 14:15:00');
INSERT INTO users (user_id, username, email, created_at)
VALUES (6, 'frankie_kim', 'frankie.kim@example.com', '2026-09-06 15:30:00');
INSERT INTO users (user_id, username, email, created_at)
VALUES (7, 'gray_williams', 'gray.williams@example.com', '2026-09-07 16:45:00');
INSERT INTO users (user_id, username, email, created_at)
VALUES (8, 'harper_singh', 'harper.singh@example.com', '2026-09-08 18:00:00');
INSERT INTO users (user_id, username, email, created_at)
VALUES (9, 'indigo_brown', 'indigo.brown@example.com', '2026-09-09 19:15:00');
INSERT INTO users (user_id, username, email, created_at)
VALUES (10, 'jules_garcia', 'jules.garcia@example.com', '2026-09-10 20:30:00');

INSERT INTO posts (post_id, user_id, title, body, published_at)
VALUES (1, 1, 'Welcome to the community', 'An introduction from Alex.', '2026-09-03 08:00:00');
INSERT INTO posts (post_id, user_id, title, body, published_at)
VALUES (2, 2, 'SQL joins made clear', 'A short guide to joining related tables.', '2026-09-05 09:30:00');
INSERT INTO posts (post_id, user_id, title, body, published_at)
VALUES (3, 3, 'Cleaning data with pandas', 'Practical tips for missing values.', '2026-09-07 11:00:00');
INSERT INTO posts (post_id, user_id, title, body, published_at)
VALUES (4, 4, 'Parameterized queries', 'Why query parameters keep applications safer.', '2026-09-10 12:30:00');
INSERT INTO posts (post_id, user_id, title, body, published_at)
VALUES (5, 5, 'Designing useful schemas', 'Choosing keys and column types.', '2026-09-12 14:00:00');
INSERT INTO posts (post_id, user_id, title, body, published_at)
VALUES (6, 6, 'ETL pipeline notes', 'Lessons learned from a first pipeline.', '2026-09-14 15:30:00');
INSERT INTO posts (post_id, user_id, title, body, published_at)
VALUES (7, 7, 'Database indexes', 'A beginner-friendly look at indexes.', '2026-09-16 17:00:00');
INSERT INTO posts (post_id, user_id, title, body, published_at)
VALUES (8, 8, 'Testing data workflows', 'Simple checks that catch common mistakes.', '2026-09-18 18:30:00');
INSERT INTO posts (post_id, user_id, title, body, published_at)
VALUES (9, 9, 'Working with CSV files', 'How to move tabular data reliably.', '2026-09-20 20:00:00');
INSERT INTO posts (post_id, user_id, title, body, published_at)
VALUES (10, 10, 'MySQL from Python', 'Connecting an application to MySQL.', '2026-09-22 21:30:00');
INSERT INTO posts (post_id, user_id, title, body, published_at)
VALUES (11, 2, 'Aggregation patterns', 'Counting records by category.', '2026-09-24 10:15:00');
INSERT INTO posts (post_id, user_id, title, body, published_at)
VALUES (12, 4, 'Draft: next steps', 'Notes for a future article.', NULL);
