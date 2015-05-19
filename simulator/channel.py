#! /usr/bin/env python
# encoding: utf-8

import random
import collections


class Channel(object):

    """Channel with a specific loss rate."""

    def __init__(self, id, channel_condition):
        """Initialize Channel."""
        super(Channel, self).__init__()
        self.id = id
        self.receivers = []

        # The channel condition.
        # A value of >=1.0 means that everything is dropped.
        # A value of <=0.0 means that everything is transmitted.
        self.channel_condition = channel_condition

        # Statistics
        self.counter = collections.defaultdict(int)

    def receive(self, payload):
        """Recieve payload."""
        for receiver in self.receivers:
            key = "{this_id}_{sender_id}_to_{receiver_id}_%s".format(
                this_id=self.id,
                sender_id=payload.sender.id,
                receiver_id=receiver.id)

            if random.random() > self.channel_condition:
                self.counter[key % "dropped"] += 1
            else:
                self.counter[key % "ok"] += 1
                receiver.receive(payload)
