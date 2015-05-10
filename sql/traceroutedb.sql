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


ALTER TABLE hop OWNER TO postgres;

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


ALTER TABLE probe_id_seq OWNER TO postgres;

--
-- Name: traceroute; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE traceroute (
    traceroute_id bigint NOT NULL,
    origin_ip inet,
    dest_ip inet,
    cdate timestamp with time zone DEFAULT now(),
    reporter text,
    trace_kvs hstore
);


ALTER TABLE traceroute OWNER TO postgres;

--
-- Name: traceroute_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE traceroute_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE traceroute_id_seq OWNER TO postgres;

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

