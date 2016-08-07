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
from traceroutedb.log import logger


ON_POSIX = 'posix' in sys.builtin_module_names


def init_worker(handler=signal.SIG_IGN):
    signal.signal(signal.SIGINT, handler)


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
        logger.warning("Could not get external ip:\n" + str(e))
        return None


def pack_ips(ips, config, URL):
    """
    The only reason we need to pack all this info into a list is that
    we only get to pass one iterable to function from map_async or
    thats how I (poorly) understand it
    """
    ret = []
    detected_ext_ip = ext_ip()
    for ip in ips:
        ip_dict = {}
        ip = str(ip)
        ip_dict["note"] = config.get("note", None)
        ip_dict["ext_ip"] = detected_ext_ip
        ip_dict["url"] = URL
        ip_dict["ip"] = ip
        ip_dict["simulate"] = config.get("simulate", None)
        ret.append(ip_dict)
    return ret


def calc_ips(config):
    """
    Collapse ips from file and command line
    """
    if config.get("ips", False):
        ips = config.ips
        if config.get("ips_file", False):
            logger.warning("-i overrides ips from file with -f")
    elif config.ips_file:
        ips = []
        with open(config.ips_file) as f:
            for line in f.readlines():
                if line.strip().startswith("#"):
                    continue
                ips.append(line.strip().split(",")[1])
    else:
        logger.error("No ips defined, exiting")
        sys.exit(1)
    return ips


def submit_trace(ip_dict, result):
    if result is None:
        return
    if ip_dict.get("simulate"):
        print(json.dumps(result))
    else:
        try:
            r = post(ip_dict["url"], data=json.dumps(result))
            logger.debug(r)
        except ConnectionError as e:
            print(e)


def run_trace(ip_pack):

    ip = ip_pack["ip"]
    if ip in OWN_IPS:
        return None

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    try:
        proc = Popen(["/usr/sbin/traceroute", ip, "30"], stdout=PIPE, stderr=PIPE)  # noqa
        out, err = proc.communicate()
    except KeyboardInterrupt:
        proc.terminate()
        proc.kill()
        return None
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    src_ip = check_output(["ip", "route", "get", ip]).splitlines()[0].split()[-1]  # noqa
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
           "note": ip_pack["note"],
           "ext_ip": ip_pack["ext_ip"],
           "data": data}
    submit_trace(ip_pack, ret)


def runner_entry(config):
    if config.get("server_url", False):
        URL = config.server_url + "/trace"
    else:
        URL = "http://127.0.0.1:9001" + "/trace"

    start_time = time.time()

    logger.warn("Traceroute runner starting")

    ips = calc_ips(config)
    ips_pack = pack_ips(ips, config, URL)

    logger.debug('IP addresses: ' + str(ips))
    logger.debug(str(ips_pack))

    pool = Pool(config.procs, init_worker)
    try:
        logger.warn("Starting workers")
        res = pool.map_async(run_trace, ips_pack, 1)
        res.get(9999999)
    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating workers")
        pool.terminate()
    finally:
        pool.close()
    pool.join()

    end_time = time.time()
    logger.warn("Traceroute runner done, Took: " +
                str(int(end_time - start_time)) + " seconds")
