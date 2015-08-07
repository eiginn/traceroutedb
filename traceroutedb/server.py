#!/usr/bin/env python

from __future__ import print_function
import psycopg2
from flask import Flask, request
from argparse import ArgumentParser
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

parser = ArgumentParser()
parser.add_argument("-d", "--debug", help="debug mode", action="store_true")
args = parser.parse_args()

if args.debug:
    logger.setLevel(logging.DEBUG)


def dictToHstore(in_dict):
    single_kvs = []
    for key in in_dict.iterkeys():
        single_kvs.append("{0}=>{1}".format(key, in_dict[key] if in_dict[key] else "NULL"))
    hstore_str = "'{0}'".format(", ".join(single_kvs))
    return hstore_str


@app.route('/trace', methods=["POST"])
def receive_traces():
    if request.method == 'POST':
        conn = psycopg2.connect("dbname=traceroutedb user=postgres host=localhost")
        cur = conn.cursor()
        data = request.get_json(force=True)

        trace = data["data"]
        reporter = data["reporter"]
        kvs = {"note": data.get("note"), "ext_ip": data.get("ext_ip")}

        if args.debug:
            print("SELECT nextval('traceroute_id_seq');")
            trace_id = "DEBUG_ID"
        else:
            cur.execute("SELECT nextval('traceroute_id_seq');")
            trace_id = cur.fetchone()[0]

        if args.debug:
            print("INSERT INTO traceroute VALUES ({0}, '{1}', '{2}', now(), '{3}', {4}::HSTORE);".format(trace_id, trace["src_ip"], trace["dst_ip"], reporter, dictToHstore(kvs)))
        else:
            cur.execute("INSERT INTO traceroute VALUES ({0}, '{1}', '{2}', now(), '{3}', {4}::HSTORE);".format(trace_id, trace["src_ip"], trace["dst_ip"], reporter, dictToHstore(kvs)))

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
                    cur.execute("INSERT INTO hop VALUES (nextval('probe_id_seq'), {0}, {1}, {2}, '{3}', now());".format(trace_id, key, kvs, probe["ip"]))
    conn.commit()
    cur.close()
    conn.close()
    print("ip:", request.remote_addr, "submitted result for:", trace["src_ip"], ">", trace["dst_ip"], "trace_id:", trace_id)
    return 'OK'


if __name__ == '__main__':
    app.run(port=9001, debug=args.debug)
