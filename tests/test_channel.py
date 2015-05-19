#! /usr/bin/env python
# encoding: utf-8

from nose.tools import *
import simulation.channel


def test_instatiation():
    id = "test_id"
    channel_condition = 0.5
    c = simulation.channel.Channel(id, channel_condition)
    assert_equal(c.id, id)
    assert_equal(c.channel_condition, channel_condition)
