#! /usr/bin/env python
# encoding: utf-8

from . import receiver


class Sink(object):
    """Sink."""

    def __init__(self, id, stats, decoder):
        """Initialize Sink."""
        super(Sink, self).__init__()
        self.receiver = receiver.Receiver(id, stats, decoder)

    def receive(self, payload):
        """Recieve payload."""
        self.receiver.receive(payload)
