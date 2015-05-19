#! /usr/bin/env python
# encoding: utf-8

from nose.tools import *
import simulation.relay


def test_instatiation():
    id = "test_id"
    decoder = "decoder_object"
    c = simulation.relay.Relay(id, decoder)
    assert_equal(c.id, id)
    assert_equal(c.decoder, decoder)
