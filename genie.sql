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
  id integer NOT NULL,
  name character varying NOT NULL,
  year integer NOT NULL,
  count integer NOT NULL DEFAULT 0
);

CREATE SEQUENCE public.entities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.entities_id_seq OWNED BY public.entities.id;

CREATE UNIQUE INDEX index_entities_on_name_and_year ON public.entities USING btree (name, year);
