-- public.media definition

-- Drop table

-- DROP TABLE public.media;

CREATE TABLE public.media (
	hash varchar NOT NULL,
	CONSTRAINT media_pk PRIMARY KEY (hash)
);


-- public.users definition

-- Drop table

-- DROP TABLE public.users;

CREATE TABLE public.users (
	username varchar NOT NULL,
	display_name varchar NOT NULL,
	email varchar NOT NULL,
    password varchar NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY (username)
);


-- public.posts definition

-- Drop table

-- DROP TABLE public.posts;

CREATE TABLE public.posts (
	id uuid NOT NULL,
	title varchar NOT NULL,
	body varchar NOT NULL,
	author varchar NOT NULL,
	reply_to uuid NULL,
	posted_at timestamptz NOT NULL DEFAULT now(),
	CONSTRAINT posts_pk PRIMARY KEY (id),
	CONSTRAINT posts_posts_fk FOREIGN KEY (reply_to) REFERENCES public.posts(id) ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED,
	CONSTRAINT posts_users_fk FOREIGN KEY (author) REFERENCES public.users(username) ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED
);


-- public.reaction definition

-- Drop table

-- DROP TABLE public.reaction;

CREATE TABLE public.reaction (
	post uuid NOT NULL,
	author varchar NOT NULL,
	"character" varchar NOT NULL,
	CONSTRAINT reaction_pk PRIMARY KEY (post, author, "character"),
	CONSTRAINT reaction_posts_fk FOREIGN KEY (post) REFERENCES public.posts(id) ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED,
	CONSTRAINT reaction_users_fk FOREIGN KEY (author) REFERENCES public.users(username) ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED
);


-- public.post_media definition

-- Drop table

-- DROP TABLE public.post_media;

CREATE TABLE public.post_media (
	id serial4 NOT NULL,
	media varchar NOT NULL,
	post uuid NULL,
	CONSTRAINT post_media_pk PRIMARY KEY (id),
	CONSTRAINT post_media_media_fk FOREIGN KEY (media) REFERENCES public.media(hash) ON DELETE RESTRICT ON UPDATE RESTRICT,
	CONSTRAINT post_media_posts_fk FOREIGN KEY (post) REFERENCES public.posts(id) ON DELETE SET NULL ON UPDATE CASCADE
);


-- public.reactions_count source

CREATE MATERIALIZED VIEW public.reactions_count
TABLESPACE pg_default
AS SELECT post,
    "character",
    count(*) AS count
   FROM reaction
  GROUP BY post, "character"
WITH DATA;