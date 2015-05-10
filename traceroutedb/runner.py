#!/usr/bin/env python

from __future__ import print_function
import sys
import json
import socket
import time
import tracerouteparser
from argparse import ArgumentParser
from requests import post
from requests import ConnectionError
from subprocess import check_output
import logging


parser = ArgumentParser()
parser.add_argument("-d", "--debug", help="debug mode", action="store_true")
parser.add_argument("-r", "--read-file",
                    help="read ips from file one per line",
                    type=str, dest="ips_file")
parser.add_argument("-s", "--server",
                    help="server to send traces to",
                    type=str, dest="server", default=False)
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG)
start_time = time.time()
logging.info("Traceroute runner starting")

dump = {}
if args.server:
    url = args.server
else:
    url = 'http://127.0.0.1:9001/trace'
dump["reporter"] = socket.gethostname()
ips = []

if args.ips_file:
    with open(args.ips_file) as f:
        for line in f:
            ips.append(line.strip())
else:
    ips.append('8.8.8.8')

own_ips = check_output(["ip", "-4", "addr", "list"])

logging.debug('IP addresses:\n' + str(ips))

for ip in ips:
    dump["data"] = []

    if ip in own_ips:
        continue
    logging.info(ip)
    size = "20"
    out = check_output(["/usr/sbin/traceroute", ip, size])
    src_ip = check_output(["ip", "route", "get", ip]).splitlines()[0].split()[-1]
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

    if args.debug:
        logging.debug(json.dumps(dump))
    else:
        try:
            r = post(url, data=json.dumps(dump))
        except ConnectionError as e:
            print(e)

end_time = time.time()
logging.info("Traceroute runner done, Took: " + str(int(end_time - start_time)) + " seconds")
