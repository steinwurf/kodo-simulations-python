#! /usr/bin/env python
# encoding: utf-8

import os

from . import packet
from . import sender


class Source(object):
    """Source."""

    def __init__(self, id, stats, encoder):
        """Initialize Source."""
        super(Source, self).__init__()
        self.sender = sender.Sender(id)

        self.encoder = encoder
        self.stats = stats

        # Generate some random data to encode. We create a bytearray of the
        # same size as the encoder's block size and assign it to the encoder.
        # This bytearray must not go out of scope while the encoder exists!
        self.data_in = bytearray(os.urandom(self.encoder.block_size()))
        self.encoder.set_symbols_storage(self.data_in)

    def tick(self):
        """Increment time."""
        self.stats["source_sent"] += 1

        payload_data = self.encoder.produce_payload()
        p = packet.Packet(self, payload_data)
        self.sender.send(p)
