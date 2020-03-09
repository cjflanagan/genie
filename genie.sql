CREATE DATABASE genie;

\c genie;

CREATE TABLE public.articles(
  id character(16) PRIMARY KEY NOT NULL,
  filename character(64) NOT NULL,
  published_at timestamp without time zone NOT NULL,
  processed boolean NOT NULL DEFAULT false,
  created_at timestamp without time zone NOT NULL,
  updated_at timestamp without time zone NOT NULL
);

CREATE UNIQUE INDEX index_articles_on_id ON public.articles USING btree (id);

CREATE TABLE public.entities(
  id character varying PRIMARY KEY NOT NULL,
  count integer NOT NULL
);

CREATE UNIQUE INDEX index_entities_on_id ON public.entities USING btree (id);
