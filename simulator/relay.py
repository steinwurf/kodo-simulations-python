#! /usr/bin/env python
# encoding: utf-8

import copy

from . import packet
from . import receiver
from . import sender


class Relay(object):

    """Relay."""

    def __init__(self, id, stats, decoder):
        """Initialize Relay."""
        super(Relay, self).__init__()

        self.receiver = receiver.Receiver(id, stats, decoder)
        self.sender = sender.Sender(id)

        # Recode or simply forward packets
        self.recode_on = True

        # Transmit in every tick, or only when a packet is received from sink
        self.transmit_every_tick = True

        # We store the last packet for forwarding
        self.packet = None

    def receive(self, payload):
        """Recieve payload."""
        self.packet = copy.copy(payload)
        self.receiver.receive(payload)

    def tick(self):
        """Increment time."""
        # Only transmit if we got something to transmit.
        if not self.packet:
            return

        # We send a packet either:
        # 1) We are transmitting on receive and we got a packet
        # 2) We always transmit on every tick
        p = None
        if self.recode_on:
            recode_buffer = self.receiver.decoder.write_payload()
            p = packet.Packet(self, recode_buffer)
        else:
            self.packet.sender = self
            p = self.packet

        self.sender.send(p)

        if not self.transmit_every_tick:
            self.packet = None
