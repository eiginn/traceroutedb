#!/usr/bin/env python

from __future__ import print_function
import sys
import json
import socket
import time
import ezcf
import tracerouteparser
import signal
from argparse import ArgumentParser
from requests import post, get, ConnectionError
from subprocess import check_output
from multiprocessing import Pool
import logging


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def ext_ip():
    try:
        resp = get('https://httpbin.org/ip')
        return resp.json()["origin"]
    except ConnectionError as e:
        logging.warning("Could not get external ip:\n" + e)
        return None


def submit_trace(result):
    if result is None:
        return
    if args.simulate:
        logging.debug(json.dumps(result))
    else:
        try:
            r = post(URL, data=json.dumps(result))
            logging.debug(r)
        except ConnectionError as e:
            print(e)


def run_trace(ip):
    if ip in OWN_IPS:
        return None
    out = check_output(['/usr/sbin/traceroute', ip, "30"])
    src_ip = check_output(["ip", "route", "get", ip]).splitlines()[0].split()[-1]
    trp = tracerouteparser.TracerouteParser()
    trp.parse_data(out)
    data = {}
    data["dst_ip"] = trp.dest_ip
    data["src_ip"] = src_ip
    data["dst_name"] = trp.dest_name
    data["hops"] = {}

    for hop in trp.hops:
        data["hops"][int(hop.idx)] = []
        for probe in hop.probes:
            data["hops"][int(hop.idx)].append({"name": probe.name,
                                               "ip": probe.ipaddr,
                                               "rtt": probe.rtt,
                                               "anno": probe.anno})
    ret = {"reporter": socket.gethostname(),
           "note": NOTE,
           "ext_ip": EXT_IP,
           "data": data}
    submit_trace(ret)


parser = ArgumentParser()
parser.add_argument("-d", "--debug", help="debug mode", action="store_true")
parser.add_argument("-S", "--simulate", help="Simulate and don't submit results", action="store_true")
parser.add_argument("-r", "--read-file",
                    help="read ips from file one per line",
                    type=str, dest="ips_file")
parser.add_argument("-i", "--ip", help="dst ip for trace, can be givven multiple times",
                    dest="ips", action="append")
parser.add_argument("-s", "--server",
                    help="server to send traces to",
                    type=str, dest="server", default=False)
parser.add_argument("-c", "--config",
                    help="path to config file",
                    type=str, dest="conf_file")
parser.add_argument("-N", "--note",
                    help="trace note",
                    type=str, dest="trace_note")
parser.add_argument("-p", "--procs",
                    help="num procs",
                    default=10,
                    type=int, dest="numprocs")
args = parser.parse_args()

ON_POSIX = 'posix' in sys.builtin_module_names
NUMPROCS = args.numprocs
global OWN_IPS
OWN_IPS = check_output(["ip", "-4", "addr", "list"])

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
start_time = time.time()

if args.conf_file:
    FIX_IMPORT_WARNING = ezcf
    conf = __import__(args.conf_file)

logging.info("Traceroute runner starting")

global URL
if args.server:
    URL = args.server
else:
    URL = 'http://127.0.0.1:9001/trace'

global EXT_IP
EXT_IP = ext_ip()

NOTE = args.trace_note if args.trace_note else None

if args.ips:
    ips = args.ips
    if args.ips_file:
        logging.warning("-i overrides ips from file with -r")
elif args.ips_file:
    ips = []
    with open(args.ips_file) as f:
        for line in f:
            ips.append(line.strip())
else:
    ips = ["8.8.8.8"]


logging.debug('IP addresses: ' + str(ips))

pool = Pool(NUMPROCS, init_worker)
try:
    pool.map_async(run_trace, ips, 1).get(9999999)
except KeyboardInterrupt:
    print("Caught KeyboardInterrupt, terminating workers")
    pool.terminate()
    sys.exit(1)

pool.close()
pool.join()

end_time = time.time()
logging.info("Traceroute runner done, Took: " + str(int(end_time - start_time)) + " seconds")
