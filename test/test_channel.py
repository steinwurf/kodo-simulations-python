#! /usr/bin/env python
# encoding: utf-8

import sys
sys.path.append('..')

import unittest
import simulator.channel

class TestChannel(unittest.TestCase):

    def test_instantiation(self):
        id = "test_id"
        stats = {}
        channel_condition = 0.5
        c = simulator.channel.Channel(id, stats, channel_condition)
        self.assertEqual(c.id, id)
        self.assertEqual(c.channel_condition, channel_condition)

if __name__ == '__main__':
    unittest.main()
