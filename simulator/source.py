#! /usr/bin/env python
# encoding: utf-8

import packet
import sender
import os


class Source(object):

    """Source."""

    def __init__(self, id, stats, encoder):
        """Initialize Source."""
        super(Source, self).__init__()
        self.sender = sender.Sender(id)

        self.encoder = encoder
        self.stats = stats

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
        self.stats["source_sent"] += 1

        payload_data = self.encoder.write_payload()
        p = packet.Packet(self, payload_data)
        self.sender.send(p)
