#! /usr/bin/env python
# encoding: utf-8

import collections
import packet


class Relay(object):

    """Relay."""

    def __init__(self, id, decoder):
        """Initialize Relay."""
        super(Relay, self).__init__()
        self.id = id
        self.receivers = []

        # Decoder used by the relay to recode
        self.decoder = decoder

        # Recode or simply forward packets
        self.recode_on = True

        # Relay should transmit in every tick, or when a packet is received
        # from sink
        self.transmit_on_receive = False

        # We store the last packet for forwarding
        self.new_packet = False
        self.last_packet = None

        # Statistics
        self.counter = collections.defaultdict(int)

    def receive(self, payload):
        """Recieve payload."""
        self.last_packet = payload
        self.new_packet = True

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

    def tick(self):
        """Increment time."""
        if self.transmit_on_receive and not self.new_packet:
            # In this mode we only transmit if we got an packet
            return

        # We send a packet either:
        # 1) We are transmitting on receive and we got a packet
        # 2) We always transmit on every tick

        if self.recode_on:
            recode_buffer = self.decoder.write_payload()
            p = packet.Packet(self, recode_buffer)
            for receiver in self.receivers:
                receiver.receive(p)

        else:
            if self.last_packet.is_valid() != True:
                return

            self.last_packet.sender = self
            for receiver in self.receivers:
                receiver.receive(self.last_packet)

        self.new_packet = False
