-- Show published posts from the second half of September with their authors.
SELECT
    p.post_id,
    u.username,
    p.title,
    p.published_at
FROM posts AS p
INNER JOIN users AS u
    ON p.user_id = u.user_id
WHERE p.published_at >= '2026-09-15 00:00:00'
ORDER BY p.published_at;
