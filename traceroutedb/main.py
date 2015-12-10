#!/usr/bin/env python

import click
import yaml
from config import Config


@click.group()
@click.option("-c", "--configfile", type=click.File("r"), help="")
@click.option("-d", "--debug", is_flag=True, default=False, help="")
@click.option("-S", "--simulate", is_flag=True, default=False, help="")
@click.option("-v", "--verbose", default=0, help="", count=True)
@click.pass_context
def cli(ctx, configfile, debug, simulate, verbose):
    config = ctx.obj["config"]
    if configfile:
        config.update(yaml.safe_load(configfile))
    config.verbose = verbose
    config.debug = debug
    config.simulate = simulate
    if config.debug:
        print "config:"
        print config


@click.command()
@click.option("-f", "--ips-file", type=click.File("r"), help="read ips from file one per line")
@click.pass_context
def server(ctx, ips_file):
    config = ctx.obj["config"]
    config.ips_file = ips_file
    from traceroutedb.server import run_server
    run_server(config)


@click.command()
@click.option("-f", "--ips-file", type=click.File("r"), help="read ips from file one per line")
@click.option("-n", "--hostname", default=None, help="")
@click.option("-R", "--remote-ips", help="Use ips pulled from server", is_flag=True)
@click.option("-i", "--ip", help="dst ip for trace, can be given multiple times", multiple=True, type=str)
@click.option("-s", "--server", help="server to send traces to")
@click.option("-N", "--note", help="trace note")
@click.option("-P", "--procs", type=int, default=10, help="num procs")
@click.pass_context
def runner(ctx, ips_file, hostname, remote_ips, ip, server, note, procs):
    config = ctx.obj["config"]
    config.ips_file = ips_file
    config.hostname = hostname
    config.remote_ips = remote_ips
    config.ips = ip
    config.server = server
    config.note = note
    config.procs = procs
    from traceroutedb.runner import run_runner
    run_runner(config)


def cli_entry():
    cli.add_command(server)
    cli.add_command(runner)
    cli(obj={"config": Config()})


if __name__ == "__main__":
    cli_entry()
