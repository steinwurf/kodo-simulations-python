#! /usr/bin/env python
# encoding: utf-8

import sys
sys.path.append('..')
sys.path.append('mock')

import unittest
from mock import Mock
import simulator.sink


class TestSink(unittest.TestCase):
    """Class for testing Sink."""

    def test_instantiation(self):
        """Test instantiation."""
        id = "test_id"
        stats = {}
        decoder = Mock(name="decoder_object")
        decoder.block_size = Mock(return_value=100)
        c = simulator.sink.Sink(id, stats, decoder)
        self.assertEqual(c.receiver.id, id)
        self.assertEqual(c.receiver.decoder, decoder)

if __name__ == '__main__':
    unittest.main()
