#! /usr/bin/env python
# encoding: utf-8

from nose.tools import *
import simulation.packet


def test_instatiation():
    sender = "sender object"
    data = "test_data"
    c = simulation.packet.Packet(sender, data)
    assert_equal(c.sender, sender)
    assert_equal(c.data, data)
