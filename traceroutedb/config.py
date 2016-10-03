import os
import sys


class Config(dict):

    def __init__(self):
        dict.__init__(self)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        del self[key]

    def __repr__(self):
        return '<Config ' + dict.__repr__(self) + '>'


def create_config():
    default = """\
verbose: False
debug: False
simulate: False

server:
  ips_file: "/etc/trdb/endpoints"
  mmdb: "/etc/trdb/GeoIP2-ISP.mmdb"
  bind: 127.0.0.1
  port: 9001

runner:
  ips_file: "/etc/trdb/endpoints"
  # hostname: ""
  remote_ips: False
  # will overide ips_file and ips from server (remote_ips)
  # ips:
  #   - "8.8.8.8"
  #   - "1.1.1.1"
  server_url: "http://127.0.0.1:9001"
  procs: 10
  # Multiple parsers are planned, currently the NANOG traceroute is supported,
  #     vanilla "traceroute" pkg on Debian
  # DO NOT use /usr/bin/traceroute or just traceroute, on debian the alternatives
  # system could mess this up if you have more than one traceroute installed
  traceroute_bin: /usr/bin/traceroute-nanog\n"""

    try:
        with open(os.path.expanduser("~/.trdb.yaml"), "w") as f:
            f.write(default)
    except:
        print "Failed to write out example config"
        sys.exit(1)
