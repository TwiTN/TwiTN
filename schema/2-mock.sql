-- ==================================================
-- Script : Génération de posts 10 niveaux × 2 branches
-- ==================================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

BEGIN;

-- =========================
-- Utilisateur de test
-- =========================
INSERT INTO public.users (username, display_name, email, password)
VALUES
('test_user', 'Test User', 'test_user@example.com', 'hash_test')
ON CONFLICT (username) DO NOTHING;

-- =========================
-- Génération des posts hiérarchiques
-- =========================
WITH RECURSIVE posts_recursive AS (
    -- Niveau 1 = racine (1 racine pour simplifier)
    SELECT
        uuid_generate_v5('00000000-0000-0000-0000-000000000000', 'root') AS id,
        NULL::uuid AS reply_to,
        'Post niveau 1' AS title,
        'Contenu du post niveau 1' AS body,
        'test_user' AS author,
        1 AS depth
    UNION ALL
    -- Niveaux suivants avec 2 branches par post
    SELECT
        uuid_generate_v5('00000000-0000-0000-0000-000000000000', pr.id::text || '_branch' || b.branch_index) AS id,
        pr.id AS reply_to,
        'Post niveau ' || (pr.depth+1) || ', branche #' || b.branch_index AS title,
        'Contenu du post niveau ' || (pr.depth+1) AS body,
        pr.author AS author,
        pr.depth + 1 AS depth
    FROM posts_recursive pr
    CROSS JOIN (VALUES (1), (2)) AS b(branch_index)
    WHERE pr.depth < 11
)
INSERT INTO public.posts (id, title, body, author, reply_to, posted_at)
SELECT id, title, body, author, reply_to, now()
FROM posts_recursive
ORDER BY depth, id;

COMMIT;
