#! /usr/bin/env python
# encoding: utf-8

import collections

from . import source
from . import relay
from . import sink
from . import channel


class Simulator(object):
    """Simulator."""

    def __init__(self, encoder_type, decoder_type, field, symbols,
                 symbol_size):
        """Initialize Simulator."""
        super(Simulator, self).__init__()
        self.encoder_type = encoder_type
        self.decoder_type = decoder_type
        self.field = field
        self.symbols = symbols
        self.symbol_size = symbol_size

        self.sources = []
        self.sinks = []
        self.relays = []

        self.nodes = []

        self.id_indicies = collections.defaultdict(int)
        self.results = collections.defaultdict(int)

    def create_source(self, id=None):
        """Create Source."""
        if not id:
            id = self.__generate_name("source")
        encoder = self.encoder_type(
            self.field, self.symbols, self.symbol_size)
        s = source.Source(id, self.results, encoder)
        self.nodes.append(s)
        self.sources.append(s)
        return s

    def create_relay(self, id=None):
        """Create Relay."""
        if not id:
            id = self.__generate_name("relay")
        decoder = self.decoder_type(
            self.field, self.symbols, self.symbol_size)
        r = relay.Relay(id, self.results, decoder)
        self.nodes.append(r)
        self.relays.append(r)
        return r

    def create_sink(self, id=None):
        """Create Sink."""
        if not id:
            id = self.__generate_name("sink")
        decoder = self.decoder_type(
            self.field, self.symbols, self.symbol_size)
        s = sink.Sink(id, self.results, decoder)
        self.nodes.append(s)
        self.sinks.append(s)
        return s

    def create_channel(self, channel_condition=0.0, id=None):
        """Create Channel."""
        if not id:
            id = self.__generate_name("channel")
        c = channel.Channel(id, self.results, channel_condition)
        self.nodes.append(c)
        return c

    def connect(self, channel, a, b):
        """
        Connect two nodes with a channel.

        Connects node a to node b using the given channel.
        """
        a.sender.channels.append(channel)
        channel.receivers.append(b)

    def run(self, done):
        """Run simulator."""
        senders = self.sources + self.relays
        while not done():
            for sender in senders:
                sender.tick()

    def get_statistics(self):
        """Get statistics collected during run."""
        return self.results

    def __generate_name(self, prefix):
        index = self.id_indicies[prefix]
        self.id_indicies[prefix] += 1
        return "{}{}".format(prefix, index)
