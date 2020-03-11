CREATE DATABASE genie;

\c genie;

CREATE TABLE public.articles(
  id character varying PRIMARY KEY NOT NULL,
  filename character varying NOT NULL,
  published_at timestamp without time zone NOT NULL,
  processed boolean NOT NULL DEFAULT false,
  created_at timestamp without time zone NOT NULL,
  updated_at timestamp without time zone NOT NULL
);

CREATE INDEX index_articles_on_published_at ON public.articles USING btree (published_at);
CREATE INDEX index_articles_on_processed ON public.articles USING btree (processed);

CREATE TABLE public.entities(
  name character varying NOT NULL,
  year integer NOT NULL,
  count integer NOT NULL DEFAULT 0,
  PRIMARY KEY(name, year)
);
