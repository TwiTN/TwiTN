CREATE OR REPLACE FUNCTION get_post_tree(
    p_root_id   UUID,
    p_max_depth INT
)
RETURNS TABLE (
    id        UUID,
    title     VARCHAR,
    body      VARCHAR,
    author    VARCHAR,
    reply_to  UUID,
    depth     INT
)
LANGUAGE sql
AS $$
WITH RECURSIVE post_tree AS (
    -- On récupère la racine de l'arbre (post initial) avec une profondeur de 0
    SELECT
        p.*,
        0 AS depth
    FROM posts p
    WHERE p.id = p_root_id

    UNION ALL

    -- On récupère récursivement les réponses aux posts précédents, en augmentant la profondeur à chaque niveau
    SELECT
        p.*,
        pt.depth + 1
    FROM post_tree pt
    JOIN posts p ON p.reply_to = pt.id
    WHERE pt.depth < p_max_depth
)
SELECT *
FROM post_tree
ORDER BY depth, id;
$$;


CREATE INDEX idx_posts_reply_to ON posts(reply_to);