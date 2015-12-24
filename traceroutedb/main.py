#!/usr/bin/env python

import click
import yaml
import json
from config import Config


@click.group()
@click.option("-c", "--configfile", type=str, help="path to yaml config file")
@click.option("-d", "--debug", is_flag=True, default=False, help="debug mode")
@click.option("-S", "--simulate", is_flag=True, default=False, help="take no actions")
@click.option("-v", "--verbose", default=0, count=True, help="verbose, can be given multiple times")
@click.pass_context
def cli(ctx, configfile, debug, simulate, verbose):
    config = ctx.obj["config"]
    if configfile:
        with open(configfile, "r") as f:
            config.update(yaml.safe_load(f))
    config.verbose = verbose
    config.debug = debug
    config.simulate = simulate
    if config.debug:
        print "config:"
        print json.dumps(config, indent=2)


@click.command()
@click.option("-f", "--ips-file", type=str, help="read ips from file one per line")
@click.option("--mmdb", type=str, help="path to mmdb for isp lookup")
@click.pass_context
def server(ctx, ips_file, mmdb):
    config = ctx.obj["config"]
    config.update(config.pop("server", {}))
    if ips_file:
        config.ips_file = ips_file
    if mmdb:
        config.mmdb = mmdb
    from traceroutedb.server import run_server
    run_server(config)


@click.command()
@click.option("-f", "--ips-file", type=str, help="read ips from file one per line")
@click.option("-n", "--hostname", default=None, help="reported hostname of this machine (reporter)")
@click.option("-R", "--remote-ips", is_flag=True, help="Use ips pulled from server")
@click.option("-i", "--ip", multiple=True, type=str, help="dst ip for trace, can be given multiple times")
@click.option("-s", "--server_url", help="server to send traces to (http://$server_port)")
@click.option("-N", "--note", help="trace note")
@click.option("-P", "--procs", type=int, help="num procs")
@click.pass_context
def runner(ctx, ips_file, hostname, remote_ips, ip, server_url, note, procs):
    config = ctx.obj["config"]
    config.update(config.pop("runner", {}))
    if ips_file:
        config.ips_file = ips_file
    if hostname:
        config.hostname = hostname
    if remote_ips:
        config.remote_ips = remote_ips
    if ip:
        config.ips = ip
    if server_url:
        config.server_url = server_url
    if note:
        config.note = note
    if procs:
        config.procs = procs
    else:
        config.procs = 10
    from traceroutedb.runner import run_runner
    run_runner(config)


def cli_entry():
    cli.add_command(server)
    cli.add_command(runner)
    cli(obj={"config": Config()})


if __name__ == "__main__":
    cli_entry()
