--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: hstore; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS hstore WITH SCHEMA public;


--
-- Name: EXTENSION hstore; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION hstore IS 'data type for storing sets of (key, value) pairs';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: hop; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE hop (
    probe_id bigint NOT NULL,
    traceroute_id bigint,
    hop_number integer,
    hop_kvs hstore,
    host character varying,
    cdate timestamp with time zone
);


ALTER TABLE public.hop OWNER TO postgres;

--
-- Name: COLUMN hop.hop_kvs; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN hop.hop_kvs IS 'Time in milliseconds AND annotation';


--
-- Name: probe_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE probe_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.probe_id_seq OWNER TO postgres;

--
-- Name: traceroute; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE traceroute (
    traceroute_id bigint NOT NULL,
    origin_ip inet,
    dest_ip inet,
    cdate timestamp with time zone DEFAULT now(),
    reporter text
);


ALTER TABLE public.traceroute OWNER TO postgres;

--
-- Name: traceroute_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE traceroute_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.traceroute_id_seq OWNER TO postgres;

--
-- Name: hop_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY hop
    ADD CONSTRAINT hop_pkey PRIMARY KEY (probe_id);


--
-- Name: traceroute_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY traceroute
    ADD CONSTRAINT traceroute_pkey PRIMARY KEY (traceroute_id);


--
-- Name: uni_hop_id; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY hop
    ADD CONSTRAINT uni_hop_id UNIQUE (probe_id);


--
-- Name: uni_id; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY traceroute
    ADD CONSTRAINT uni_id UNIQUE (traceroute_id);


--
-- Name: hop_traceroute_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY hop
    ADD CONSTRAINT hop_traceroute_id_fkey FOREIGN KEY (traceroute_id) REFERENCES traceroute(traceroute_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

CREATE OR REPLACE FUNCTION trace_add(__src_ip INET, __dst_ip INET, __reporter VARCHAR, OUT __traceroute_id BIGINT) AS $_$
DECLARE
    __traceroute_id BIGINT;
BEGIN

    IF (__src_ip IS NULL) OR (__dst_ip IS NULL) OR (__reporter IS NULL) THEN
        __traceroute_id := -1;
        RETURN;
    ELSE
        SELECT INTO __traceroute_id nextval('traceroute_id_seq'::regclass);
        INSERT INTO traceroute VALUES (__traceroute_id, __src_ip, __dst_ip, now(), __reporter);
    RETURN;
END;
$_$ Language 'plpgsql' SECURITY DEFINER;

CREATE OR REPLACE FUNCTION hop_add(__probe_id INT, __traceroute_id BIGINT, __hop_num INT, __hop_kvs HSTORE, OUT __hop_id) AS $_$
DECLARE
    __hop_id BIGINT;
BEGIN

    IF (__probe_id IS NULL) OR (__traceroute_id IS NULL) OR (__hop_num IS NULL) OR (__hop_kvs IS NULL) THEN
        __hop_id := -1;
        RETURN;
    ELSE
        -- BLAH
    RETURN;
END;
$_$ Language 'plpgsql' SECURITY DEFINER;
