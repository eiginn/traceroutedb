#!/usr/bin/env python

from __future__ import print_function
import sys
import json
import socket
import time
import tracerouteparser
import signal
from requests import post, get, ConnectionError
from subprocess import check_output, Popen, PIPE
from multiprocessing import Pool
import logging


ON_POSIX = 'posix' in sys.builtin_module_names


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def own_ips():
    return check_output(["ip", "-4", "addr", "list"])


global OWN_IPS
OWN_IPS = own_ips()


def ext_ip():
    """
    We make the assumtion that we ony have one gateway to any one destination,
    could be better to use "ip route get $ip" but that won't cover NAT scenario
    """
    try:
        resp = get('https://httpbin.org/ip')
        return resp.json()["origin"]
    except ConnectionError as e:
        logging.warning("Could not get external ip:\n" + str(e))
        return None


def submit_trace(ip_dict, result):
    if result is None:
        return
    if ip_dict["config"].simulate:
        logging.debug(json.dumps(result))
    else:
        try:
            r = post(ip_dict["url"], data=json.dumps(result))
            logging.debug(r)
        except ConnectionError as e:
            print(e)


def run_trace(ip_dict):
    ip = ip_dict["ip"]
    if ip in OWN_IPS:
        return None
    try:
        proc = Popen(["/usr/sbin/traceroute", ip, "30"], stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
    except KeyboardInterrupt:
        proc.terminate()
        proc.kill()
        return None
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
           "note": ip_dict["note"],
           "ext_ip": ip_dict["ext_ip"],
           "data": data}
    submit_trace(ip_dict, ret)


def runner(config):
    NUMPROCS = config.procs

    if config.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("requests").setLevel(logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)
    start_time = time.time()

    logging.info("Traceroute runner starting")

    if config.server:
        URL = "http://" + config.server + "/trace"
    else:
        URL = "http://" + "127.0.0.1:9001" + "/trace"

    note = config.note if config.note else None

    if config.ips:
        ips = config.ips
        if config.ips_file:
            logging.warning("-i overrides ips from file with -f")
    elif config.ips_file:
        ips = []
        with open(config.ips_file) as f:
            for line in f:
                ips.append(line.strip())
    else:
        logging.error("No ips defined, exiting")
        sys.exit(1)

# The only reason we need to pack all this info into a list is that
# we only get to pass one iterable to function from map_async or
# thats how I (poorly) understand it
    ips_to_iter = []
    for ip in ips:
        ip_dict = {}
        ip = str(ip)
        ip_dict["config"] = config
        ip_dict["note"] = note
        ip_dict["ext_ip"] = ext_ip()
        ip_dict["url"] = URL
        ip_dict["ip"] = ip
        ips_to_iter.append(ip_dict)

    logging.debug('IP addresses: ' + str(ips))
    logging.debug(str(ips_to_iter))

    try:
        pool = Pool(NUMPROCS, init_worker)
        pool.map_async(run_trace, ips_to_iter, 1).get(9999999)
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating workers")
        pool.terminate()
        pool.join()
        sys.exit(1)

    end_time = time.time()
    logging.info("Traceroute runner done, Took: " + str(int(end_time - start_time)) + " seconds")
