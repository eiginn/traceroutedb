#!/usr/bin/env python

import click
import yaml
from config import Config


@click.group()
@click.option("-n", "--name", default=None, envvar="TRDBNAME", help="")
@click.option("-c", "--configfile", type=click.File("r"), help="")
@click.option("-d", "--debug", is_flag=True, default=False, help="")
@click.option("-S", "--simulate", is_flag=True, default=False, help="")
@click.option("-v", "--verbose", default=0, help="", count=True)
@click.pass_context
def cli(ctx, name, configfile, debug, simulate, verbose):
    config = ctx.obj["config"]
    if configfile:
        config.update(yaml.safe_load(configfile))
    config.verbose = verbose
    config.debug = debug
    config.simulate = simulate
    config.name = name
    if config.debug:
        print "config:"
        print config


@click.command()
@click.pass_context
def server(ctx):
    config = ctx.obj["config"]
    print "server"


@click.command()
@click.option("-f", "--ips-file", type=click.File("r"), help="read ips from file one per line")
@click.option("-R", "--remote-ips", help="Use ips pulled from server", is_flag=True)
@click.option("-i", "--ip", help="dst ip for trace, can be given multiple times", multiple=True)
@click.option("-s", "--server", help="server to send traces to")
@click.option("-N", "--note", help="trace note")
@click.option("-P", "--procs", type=int, default=10, help="num procs")
@click.pass_context
def runner(ctx):
    config = ctx.obj["config"]
    print "runner"


def cli_entry():
    cli.add_command(server)
    cli.add_command(runner)
    cli(obj={"config": Config()})


if __name__ == "__main__":
    cli_entry()
