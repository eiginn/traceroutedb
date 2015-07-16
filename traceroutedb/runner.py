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
from requests import post
from requests import ConnectionError
from subprocess import check_output
from multiprocessing import Pool
import logging


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


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
    ret = {"reporter": socket.gethostname(), "data": data}
    return ret


parser = ArgumentParser()
parser.add_argument("-d", "--debug", help="debug mode", action="store_true")
parser.add_argument("-S", "--simulate", help="Simulate and don't submit results", action="store_true")
parser.add_argument("-r", "--read-file",
                    help="read ips from file one per line",
                    type=str, dest="ips_file")
parser.add_argument("-s", "--server",
                    help="server to send traces to",
                    type=str, dest="server", default=False)
parser.add_argument("-c", "--config",
                    help="path to config file",
                    type=str, dest="conf_file")
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
ips = []

if args.ips_file:
    with open(args.ips_file) as f:
        for line in f:
            ips.append(line.strip())
else:
    ips.append('8.8.8.8')


logging.debug('IP addresses:\n' + str(ips))

pool = Pool(NUMPROCS, init_worker)
try:
    pool.map_async(run_trace, ips, 1, submit_trace).get(9999999)
except KeyboardInterrupt:
    print("Caught KeyboardInterrupt, terminating workers")
    pool.terminate()
    sys.exit(1)

pool.close()
pool.join()

end_time = time.time()
logging.info("Traceroute runner done, Took: " + str(int(end_time - start_time)) + " seconds")
