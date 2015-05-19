#! /usr/bin/env python
# encoding: utf-8

from nose.tools import *
import simulation.source


def test_instatiation():
    id = "test_id"
    encoder = "encoder_object"
    c = simulation.source.Source(id, encoder)
    assert_equal(c.id, id)
    assert_equal(c.encoder, encoder)
