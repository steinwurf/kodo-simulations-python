#! /usr/bin/env python
# encoding: utf-8


class Sender(object):

    """Sender."""

    def __init__(self, id):
        """Initialize Receiver."""
        super(Sender, self).__init__()
        self.id = id
        self.channels = []

    def send(self, packet):
        """Broadcast payload."""
        for channel in self.channels:
            channel.transfer(packet)
