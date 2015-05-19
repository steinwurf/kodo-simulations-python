#! /usr/bin/env python
# encoding: utf-8

import collections


class Sink(object):

    """Sink."""

    def __init__(self, id, decoder):
        """Initialize Sink."""
        super(Sink, self).__init__()
        self.id = id
        self.decoder = decoder
        self.counter = collections.defaultdict(int)

    def receive(self, payload):
        """Recieve payload."""
        key = "{}_receive_from_{}".format(self.id, payload.sender.id)
        self.counter[key] += 1

        if self.decoder.is_complete():
            key = "{}_waste_from_{}".format(self.id, payload.sender.id)
            self.counter[key] += 1
            return

        old_rank = self.decoder.rank()
        self.decoder.read_payload(payload.data)

        if old_rank < self.decoder.rank():
            key = "{}_innovative_from_{}".format(self.id, payload.sender.id)
            self.counter[key] += 1
        else:
            key = "{}_linear_dept_from_{}".format(self.id, payload.sender.id)
            self.counter[key] += 1
