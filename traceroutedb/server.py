#!/usr/bin/env python

from __future__ import print_function
import psycopg2
from flask import Flask, request, abort
from werkzeug.contrib.cache import SimpleCache
from argparse import ArgumentParser
import logging
import sys
import json

app = Flask(__name__)
cache = SimpleCache()
logger = logging.getLogger(__name__)

parser = ArgumentParser()
parser.add_argument("-d", "--debug", help="debug mode", action="store_true")
parser.add_argument("-r", "--read-file",
                    help="read ips from file one per line",
                    type=str, dest="ips_file")
args = parser.parse_args()

if args.debug:
    logger.setLevel(logging.DEBUG)


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
            single_kvs.append("{0}=>{1}".format(key, in_dict[key]))
    hstore_str = "'{0}'".format(", ".join(single_kvs))
    return hstore_str


@app.route("/rules", methods=["GET"])
@cached()
def get_rules():
    ret = {}
    if args.ips_file:
        ips = []
        with open(args.ips_file) as f:
            for line in f:
                ips.append(line.strip())
    else:
        ips = []
    ret["ips"] = ips
    return json.dumps(ret)


@app.route("/trace", methods=["POST"])
def receive_traces():
    if request.method == "POST":
        cur = conn.cursor()
        data = request.get_json(force=True)

        trace = data["data"]
        reporter = data["reporter"]
        kvs = {"note": data.get("note"), "ext_ip": data.get("ext_ip")}

        if args.debug:
            print("SELECT nextval('traceroute_id_seq');")
            trace_id = "DEBUG_ID"
        else:
            try:
                cur.execute("SELECT nextval('traceroute_id_seq');")
            except psycopg2.ProgrammingError as e:
                logging.error(str(e))
                conn.rollback()
                abort(503)
            trace_id = cur.fetchone()[0]

        trace_sql = "INSERT INTO traceroute VALUES ({0}, '{1}', '{2}', now(), '{3}', {4}::HSTORE);".format(trace_id, trace["src_ip"], trace["dst_ip"], reporter, dictToHstore(kvs))
        if args.debug:
            print(trace_sql)
        else:
            try:
                cur.execute(trace_sql)
            except psycopg2.ProgrammingError as e:
                logging.error(str(e))
                conn.rollback()
                abort(503)

        hops = trace["hops"]
        for key in hops.keys():
            hop = hops[key]
            for probe in hop:
                if probe["ip"] is None:
                    continue

                time = probe.get("rtt", None)
                if time is not None and time != "None":
                    time = "time=>{}".format(time)
                else:
                    time = ''

                anno = probe.get("anno", None)
                if anno:
                    anno = "anno=>{}".format(anno)

                kvs = "'{0}'".format(",".join([time, anno])) if anno else "'{0}'".format(time)
                if args.debug:
                    print("INSERT INTO hop VALUES (nextval('probe_id_seq'), {0}, {1}, {2}, '{3}', now());".format(trace_id, key, kvs, probe["ip"]))
                else:
                    try:
                        cur.execute("INSERT INTO hop VALUES (nextval('probe_id_seq'), {0}, {1}, {2}, '{3}', now());".format(trace_id, key, kvs, probe["ip"]))
                    except psycopg2.ProgrammingError as e:
                        logging.error(str(e))
                        conn.rollback()
                        abort(503)
    conn.commit()
    cur.close()
    conn.commit()
    print("ip:", request.remote_addr, "submitted result for:", trace["src_ip"], ">", trace["dst_ip"], "trace_id:", trace_id)
    return 'OK'


if __name__ == '__main__':
    try:
        conn = psycopg2.connect("dbname=traceroutedb user=postgres host=localhost")
    except psycopg2.OperationalError as e:
        logging.error(str(e))
        sys.exit(1)
    app.run(port=9001, debug=args.debug, host='::')
