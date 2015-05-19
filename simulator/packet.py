#! /usr/bin/env python
# encoding: utf-8


class Packet(object):

    """Simple packet."""

    def __init__(self, sender, data):
        """Initialize Packet."""
        super(Packet, self).__init__()
        self.sender = sender
        self.data = data
