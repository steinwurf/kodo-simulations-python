#! /usr/bin/env python
# encoding: utf-8

from nose.tools import *
import simulation.sink


def test_instatiation():
    id = "test_id"
    decoder = "decoder_object"
    c = simulation.sink.Sink(id, decoder)
    assert_equal(c.id, id)
    assert_equal(c.decoder, decoder)
