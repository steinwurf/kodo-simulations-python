#! /usr/bin/env python
# encoding: utf-8


class Receiver(object):

    """Receiver."""

    def __init__(self, id, stats, decoder):
        """Initialize Receiver."""
        super(Receiver, self).__init__()
        self.id = id
        self.decoder = decoder
        self.stats = stats

    def receive(self, payload):
        """Receive payload."""
        key = "{}_receive_from_{}".format(self.id, payload.sender.sender.id)
        self.stats[key] += 1

        if self.decoder.is_complete():
            key = "{}_waste_from_{}".format(self.id, payload.sender.sender.id)
            if key in self.stats:
                self.stats[key] += 1
            else:
                self.stats[key] = 0
            return

        old_rank = self.decoder.rank()
        self.decoder.read_payload(payload.data)

        key_template = "{}_%s_{}".format(
                self.id, payload.sender.sender.id)

        if old_rank < self.decoder.rank():
            self.stats[key_template % "innovative_from"] += 1
        else:
            self.stats[key_template % "linear_dept_from"] += 1
