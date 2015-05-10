#!/usr/bin/env python

import os
import sys
import logging
import argparse
import yaml

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', type=str)
parser.add_argument('-c', '--config', type=file)
parser.add_argument('-d', '--debug', action='store_true')
parser.add_argument('-m', '--mock', action='store_true')
parser.add_argument('-S', '--server', action='store_true')
parser.add_argument('-C', '--client', action='store_true')

args = parser.parse_args()

if args.server and args.client:
    sys.exit(1)

initial_config = {}
if args.config:
    initial_config.update(yaml.safe_load(args.config))
config = Config(args.name, initial_config)

if args.server:
    from trdb import server
    serv = server.Server(config)
    serv.run


def cli():
    pass
# parse conf
# let flags override conf
# if for runner/server
# run either
