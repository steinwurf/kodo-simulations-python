#! /usr/bin/env python
# encoding: utf-8

import sys
sys.path.append('..')

import unittest
import simulator.sink


class TestSink(unittest.TestCase):
    """Class for testing Sink."""

    def test_instantiation(self):
        """Test instantiation."""
        id = "test_id"
        stats = {}
        decoder = "decoder_object"
        c = simulator.sink.Sink(id, stats, decoder)
        self.assertEqual(c.receiver.id, id)
        self.assertEqual(c.receiver.decoder, decoder)

if __name__ == '__main__':
    unittest.main()
