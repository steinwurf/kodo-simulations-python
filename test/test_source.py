#! /usr/bin/env python
# encoding: utf-8

import sys
sys.path.append('..')
sys.path.append('mock')

import unittest
from mock import Mock
import simulator.source

class TestSource(unittest.TestCase):

    def test_instantiation(self):
        id = "test_id"
        stats = {}
        encoder = Mock(name="encoder_object")
        encoder.block_size = Mock(return_value=100)
        c = simulator.source.Source(id, stats, encoder)
        self.assertEqual(c.sender.id, id)
        self.assertEqual(c.encoder, encoder)

if __name__ == '__main__':
    unittest.main()
