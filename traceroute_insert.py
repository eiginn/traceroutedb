#!/usr/bin/env python

from __future__ import print_function
import json
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/trace', methods=["POST"])
def receive_traces():
    if request.method == 'POST':
        conn = psycopg2.connect("dbname=traceroutedb user=postgres host=localhost")
        cur = conn.cursor()
        data = request.get_json(force=True)
        print(json.dumps(data))
        for trace in data["data"]:
            cur.execute("SELECT nextval('traceroute_id_seq');")
            trace_id = cur.fetchone()[0]
            cur.execute("INSERT INTO traceroute VALUES ({0}, '{1}', '{2}', now(), '{3}');".format(trace_id, trace["src_ip"], trace["dst_ip"], data["reporter"]))

            hops = trace["hops"]
            for key in hops.keys():
                hop = hops[key]
                for probe in hop:
                    if probe["ip"] is None:
                        continue

                    time = probe.get("rtt", None)
                    if time or time != "None":
                        time = "time=>{}".format(time)
                        continue

                    anno = probe.get("anno", None)
                    if anno:
                        anno = "anno=>{}".format(anno)

                    kvs = "'{0}'".format(",".join([time, anno])) if anno else "'{0}'".format(time)
                    cur.execute("INSERT INTO hop VALUES (nextval('probe_id_seq'), {0}, {1}, {2}, '{3}', now());".format(trace_id, key, kvs, probe["ip"]))
        conn.commit()
        cur.close()
        conn.close()
        return 'OK'


if __name__ == '__main__':
    app.run(port=9001, debug=True)
