CREATE DATABASE genie;

\c genie;

DROP TABLE public.articles;
DROP TABLE public.entities;

CREATE TABLE public.articles(
  id character varying PRIMARY KEY NOT NULL,
  filename character varying NOT NULL,
  published_at timestamp without time zone NOT NULL,
  processed boolean NOT NULL DEFAULT false,
  created_at timestamp without time zone NOT NULL,
  updated_at timestamp without time zone NOT NULL
);

CREATE UNIQUE INDEX index_articles_on_id ON public.articles USING btree (id);
CREATE INDEX index_articles_on_published_at ON public.articles USING btree (published_at);
CREATE INDEX index_articles_on_processed ON public.articles USING btree (processed);

CREATE TABLE public.entities(
  id character varying PRIMARY KEY NOT NULL,
  count integer NOT NULL
);

CREATE UNIQUE INDEX index_entities_on_id ON public.entities USING btree (id);
