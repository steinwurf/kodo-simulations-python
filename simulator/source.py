#! /usr/bin/env python
# encoding: utf-8

import collections
import packet
import os


class Source(object):

    """Source."""

    def __init__(self, id, encoder):
        """Initialize Source."""
        super(Source, self).__init__()
        self.id = id
        self.receivers = []
        self.encoder = encoder
        self.counter = collections.defaultdict(int)

        # Create some data to encode. In this case we make a buffer
        # with the same size as the encoder's block size (the max.
        # amount a single encoder can encode)
        # Just for fun - fill the input data with random data
        data_in = os.urandom(encoder.block_size())

        # Assign the data buffer to the encoder so that we can
        # produce encoded symbols
        encoder.set_symbols(data_in)


    def tick(self):
        """Increment time."""
        self.counter["source_sent"] += 1

        payload_data = self.encoder.write_payload()

        p = packet.Packet(self, payload_data)
        for receiver in self.receivers:
            receiver.receive(p)
