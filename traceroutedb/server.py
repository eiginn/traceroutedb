#!/usr/bin/env python

from __future__ import print_function
from flask import Flask, request, abort
from werkzeug.contrib.cache import SimpleCache
import sys
import json
import geoip2.database
from geoip2.errors import AddressNotFoundError
from tabulate import tabulate
from traceroutedb.log import logger

try:
    import psycopg2
    from psycopg2 import extras as pgextras
except ImportError:
    print("psycopg2 needed to run server")
    sys.exit(1)

app = Flask(__name__)
cache = SimpleCache()


CACHE_TIMEOUT = 300


class cached(object):

    def __init__(self, timeout=None):
        self.timeout = timeout or CACHE_TIMEOUT

    def __call__(self, f):
        def decorator(*args, **kwargs):
            response = cache.get(request.path)
            if response is None:
                response = f(*args, **kwargs)
                cache.set(request.path, response, self.timeout)
            return response
        return decorator


def dictToHstore(in_dict):
    single_kvs = []
    for key in in_dict.iterkeys():
        if in_dict[key]:
            single_kvs.append('{0}=>"{1}"'.format(key, in_dict[key]))
    hstore_str = "'{0}'".format(", ".join(single_kvs))
    return hstore_str


@app.route("/rules", methods=["GET"])
@cached()
def get_rules():
    try:
        connv = psycopg2.connect("dbname=traceroutedb user=postgres host=localhost")
    except psycopg2.OperationalError as e:
        logger.error(str(e))
        abort(503)
    cur = connv.cursor()
    cur.execute("SELECT * FROM endpoints;")
    rows = cur.fetchall()
    connv.close()
    return json.dumps(rows)


@app.route("/trace", methods=["POST"])
def receive_traces():
    config = app.config["trdb"]
    if config.get("mmdb", False):
        reader = config["mmdb"]

    if request.method == "POST":
        cur = conn.cursor()
        data = request.get_json(force=True)

        trace = data["data"]
        reporter = data["reporter"]
        kvs = {"note": data.get("note"), "ext_ip": data.get("ext_ip")}

        if config.debug:
            print("SELECT nextval('traceroute_id_seq');")
            trace_id = "DEBUG_ID"
        else:
            try:
                cur.execute("SELECT nextval('traceroute_id_seq');")
            except psycopg2.ProgrammingError as e:
                logger.error(str(e))
                conn.rollback()
                abort(503)
            trace_id = cur.fetchone()[0]

        trace_sql = "INSERT INTO traceroute VALUES ({0}, '{1}', '{2}', now(), '{3}', {4}::HSTORE);".format(trace_id, trace["src_ip"], trace["dst_ip"], reporter, dictToHstore(kvs))
        if config.debug:
            print(trace_sql)
        else:
            try:
                cur.execute(trace_sql)
            except psycopg2.ProgrammingError as e:
                logger.error(str(e))
                conn.rollback()
                abort(503)

        hops = trace["hops"]
        for key in hops.keys():
            hop = hops[key]
            for probe in hop:
                if probe["ip"] is None or probe["rtt"] is None:
                    continue
                else:
                    try:
                        probe["isp"] = reader.isp(probe["ip"])
                    except AddressNotFoundError:
                        probe["isp"] = None

                kvs = {}
                time = probe.get("rtt", None)
                if time is not None and time != "None":
                    kvs["time"] = time

                anno = probe.get("anno", None)
                if anno:
                    kvs["anno"] = anno

                asn = probe.get("isp").raw.get("autonomous_system_number", None) if probe.get("isp") else False
                if asn:
                    kvs["asn"] = asn

                kvs = dictToHstore(kvs)
                if config.debug:
                    print("INSERT INTO hop VALUES (nextval('probe_id_seq'), {0}, {1}, {2}, '{3}', now());".format(trace_id, key, kvs, probe["ip"]))
                else:
                    try:
                        cur.execute("INSERT INTO hop VALUES (nextval('probe_id_seq'), {0}, {1}, {2}, '{3}', now());".format(trace_id, key, kvs, probe["ip"]))
                    except psycopg2.ProgrammingError as e:
                        logger.error(str(e))
                        conn.rollback()
                        abort(503)
    conn.commit()
    cur.close()
    conn.commit()
    print(request.remote_addr, "submitted result for:", trace["src_ip"], ">", trace["dst_ip"], "trace_id:", trace_id)
    return 'OK'


@app.route("/trace/<trace_id>", methods=["GET"])
def lookup_trace(trace_id):
    cur = conn.cursor(cursor_factory=pgextras.DictCursor)
    pgextras.register_hstore(cur)
    cur.execute("SELECT * FROM trv_trace WHERE traceroute_id = {id} ORDER BY traceroute_id,hop_number;".format(id=trace_id))
    rows = cur.fetchall()
    if "table" in request.args:
        headers = ["reporter", "traceroute_id", "origin_ip", "dest_ip", "probe_id",
                   "hop_number", "host", "hop_kvs"]
        return tabulate(rows, headers, tablefmt="psql")
    else:
        out = [json.dumps(x) for x in rows]
        return "\n".join(out)


try:
    conn = psycopg2.connect("dbname=traceroutedb user=postgres host=localhost")
except psycopg2.OperationalError as e:
    logger.error(str(e))
    sys.exit(1)


def run_server(config, app=app):
    app.config["trdb"] = config
    if config.mmdb:
        reader = geoip2.database.Reader(config.mmdb)
        app.config["trdb"]["mmdb"] = reader

    logger.warn("Starting sever")
    app.run(port=9001, debug=config.debug, host='::')
