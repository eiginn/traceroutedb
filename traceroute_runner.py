#!/usr/bin/env python

from __future__ import print_function
import sys
import json
import socket
import tracerouteparser
from requests import post
from requests import ConnectionError
from subprocess import check_output


dump = {}
url = 'http://127.0.0.1:9001/trace'
dump["reporter"] = socket.gethostname()
ips = []

if sys.argv[1] is not None:
    with open(sys.argv[1]) as f:
        for line in f:
            ips.append(line)
else:
    ips.append('8.8.8.8')

own_ips = check_output(["/sbin/ip", "-4", "addr", "list"])
dump["data"] = []

for ip in ips:
    if ip in own_ips:
        continue
    print(ip)
    args = ""
    size = "20"
    out = check_output(["/usr/sbin/traceroute", ip, size])
    src_ip = check_output(["/sbin/ip", "route", "get", ip]).splitlines()[0].split()[6]
    trp = tracerouteparser.TracerouteParser()
    trp.parse_data(out)

    dump_ip = {}
    dump_ip["dst_ip"] = trp.dest_ip
    dump_ip["src_ip"] = src_ip
    dump_ip["dst_name"] = trp.dest_name
    dump_ip["hops"] = {}

    for hop in trp.hops:
        dump_ip["hops"][int(hop.idx)] = []
        for probe in hop.probes:
            dump_ip["hops"][int(hop.idx)].append({"name": probe.name,
                                                  "ip": probe.ipaddr,
                                                  "rtt": probe.rtt,
                                                  "anno": probe.anno})
    dump["data"].append(dump_ip)
try:
    r = post(url, data=json.dumps(dump))
except ConnectionError as e:
    print(e)

# print(json.dumps(dump))
