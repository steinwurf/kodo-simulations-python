#! /usr/bin/env python
# encoding: utf-8

import random


class Channel(object):

    """Channel with a specific loss rate."""

    def __init__(self, id, stats, channel_condition):
        """Initialize Channel."""
        super(Channel, self).__init__()
        self.id = id
        self.receivers = []

        # The channel condition.
        # A value of >=1.0 means that everything is dropped.
        # A value of <=0.0 means that everything is transmitted.
        self.channel_condition = channel_condition

        # Statistics
        self.stats = stats

    def transfer(self, payload):
        """transfer payload."""
        for receiver in self.receivers:
            key = "{this_id}_{sender_id}_to_{receiver_id}_%s".format(
                this_id=self.id,
                sender_id=payload.sender.sender.id,
                receiver_id=receiver.receiver.id)

            if random.random() > self.channel_condition:
                self.stats[key % "dropped"] += 1
            else:
                self.stats[key % "ok"] += 1
                receiver.receive(payload)
