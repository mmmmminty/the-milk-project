--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: milks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.milks (
    uuid integer NOT NULL,
    mothers_name character varying(80) NOT NULL
);


ALTER TABLE public.milks OWNER TO postgres;

--
-- Name: milks_uuid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.milks_uuid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.milks_uuid_seq OWNER TO postgres;

--
-- Name: milks_uuid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.milks_uuid_seq OWNED BY public.milks.uuid;


--
-- Name: milks uuid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.milks ALTER COLUMN uuid SET DEFAULT nextval('public.milks_uuid_seq'::regclass);


--
-- Data for Name: milks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.milks (uuid, mothers_name) FROM stdin;
\.


--
-- Name: milks_uuid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.milks_uuid_seq', 1, false);


--
-- Name: milks milks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.milks
    ADD CONSTRAINT milks_pkey PRIMARY KEY (uuid);


--
-- PostgreSQL database dump complete
--

