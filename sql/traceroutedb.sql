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
-- Name: annotation; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE annotation (
    short_name character varying(10) NOT NULL,
    long_name character varying(100),
    icmp_code integer
);


ALTER TABLE annotation OWNER TO postgres;

--
-- Name: hop; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE hop (
    probe_id bigint NOT NULL,
    traceroute_id bigint,
    hop_number integer,
    hop_kvs hstore,
    host inet,
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
-- Name: trv_trace; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW trv_trace AS
 SELECT t.reporter,
    hop.traceroute_id,
    t.origin_ip,
    t.dest_ip,
    hop.probe_id,
    hop.hop_number,
    hop.host,
    hop.hop_kvs
   FROM (traceroute t
     JOIN hop USING (traceroute_id));


ALTER TABLE trv_trace OWNER TO postgres;

--
-- Name: annotation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY annotation
    ADD CONSTRAINT annotation_pkey PRIMARY KEY (short_name);


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
-- Name: uni_trace_id; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY traceroute
    ADD CONSTRAINT uni_trace_id UNIQUE (traceroute_id);


--
-- Name: traceroute_id_hop_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX traceroute_id_hop_idx ON hop USING btree (traceroute_id);


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

--
-- Data for Name: annotation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY annotation (short_name, long_name) FROM stdin;
!H      host unreachable
!N      network unreachable
!P      protocol unreachable
!S      source route failed
!F      fragmentation needed
!X      communication administratively prohibited
!V      host precedence violation
!C      precedence  cutoff in effect
!8      source host isolated
\.


--
-- PostgreSQL database dump complete
--
