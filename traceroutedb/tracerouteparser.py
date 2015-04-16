"""
A traceroute output parser, structuring the traceroute into a
sequence of hops, each containing individual probe results.

Courtesy of the Netalyzr project: http://netalyzr.icsi.berkeley.edu
"""
# ChangeLog
# ---------
#
# 1.0:  Initial release, tested on Linux/Android traceroute inputs only.
#       Also Python 2 only, most likely. (Send patches!)
#
# Copyright 2013 Christian Kreibich. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import cStringIO
import re

class Probe(object):
    """
    Abstraction of an individual probe in a traceroute.
    """
    def __init__(self):
        self.ipaddr = None
        self.name = None
        self.rtt = None # RTT in ms
        self.anno = None # Annotation, such as !H, !N, !X, etc

    def clone(self):
        """
        Return a copy of this probe, conveying the same endpoint.
        """
        copy = Probe()
        copy.ipaddr = self.ipaddr
        copy.name = self.name
        return copy

class Hop(object):
    """
    A traceroute hop consists of a number of probes.
    """
    def __init__(self):
        self.idx = None # Hop count, starting at 1
        self.probes = [] # Series of Probe instances

    def add_probe(self, probe):
        """Adds a Probe instance to this hop's results."""
        self.probes.append(probe)

    def __str__(self):
        res = []
        last_probe = None
        for probe in self.probes:
            if probe.name is None:
                res.append('*')
                continue
            anno = '' if probe.anno is None else ' ' + probe.anno
            if last_probe is None or last_probe.name != probe.name:
                res.append('%s (%s) %1.3f ms%s' % (probe.name, probe.ipaddr,
                                                   probe.rtt, anno))
            else:
                res.append('%1.3f ms%s' % (probe.rtt, anno))
            last_probe = probe
        return '  '.join(res)

class TracerouteParser(object):
    """
    A parser for traceroute text. A traceroute consists of a sequence of
    hops, each of which has at least one probe. Each probe records IP,
    hostname and timing information.
    """
    HEADER_RE = re.compile(r'traceroute to (\S+) \((\d+\.\d+\.\d+\.\d+)\)')

    def __init__(self):
        self.dest_ip = None
        self.dest_name = None
        self.hops = []

    def __str__(self):
        res = ['traceroute to %s (%s)' % (self.dest_name, self.dest_ip) ]
        ctr = 1
        for hop in self.hops:
            res.append('%2d  %s' % (ctr, str(hop)))
            ctr += 1
        return '\n'.join(res)

    def parse_data(self, data):
        """Parser entry point, given string of the whole traceroute output."""
        self.parse_hdl(cStringIO.StringIO(data))

    def parse_hdl(self, hdl):
        """Parser entry point, given readable file handle."""
        self.dest_ip = None
        self.dest_name = None
        self.hops = []

        for line in hdl:
            line = line.strip()
            if line == '':
                continue
            if line.lower().startswith('traceroute'):
                # It's the header line at the beginning of the traceroute.
                mob = self.HEADER_RE.match(line)
                if mob:
                    self.dest_ip = mob.group(2)
                    self.dest_name = mob.group(1)
            else:
                hop = self._parse_hop(line)
                self.hops.append(hop)

    def _parse_hop(self, line):
        """Internal helper, parses a single line in the output."""
        parts = line.split()
        hop = Hop()
        hop.idx = int(parts.pop(0))
        probe = None

        while len(parts) > 0:
            probe = self._parse_probe(parts, probe)
            if probe:
                hop.add_probe(probe)

        return hop

    def _parse_probe(self, parts, last_probe=None):
        """Internal helper, parses the next probe's results from a line."""
        try:
            probe = Probe() if last_probe is None else last_probe.clone()

            tok1 = parts.pop(0)
            if tok1 == '*':
                return probe

            tok2 = parts.pop(0)
            if tok2 == 'ms':
                # This is an additional RTT for the same endpoint we
                # saw before.
                probe.rtt = float(tok1)
                if len(parts) > 0 and parts[0].startswith('!'):
                    probe.anno = parts.pop(0)
            else:
                # This is a probe result from a different endpoint
                probe.name = tok1
                probe.ipaddr = tok2.translate(None, '()')
                probe.rtt = float(parts.pop(0))
                parts.pop(0) # Drop "ms"
                if len(parts) > 0 and parts[0].startswith('!'):
                    probe.anno = parts.pop(0)

            return probe

        except (IndexError, ValueError):
            return None
