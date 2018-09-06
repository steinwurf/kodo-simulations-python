#! /usr/bin/env python
# encoding: utf-8

import sys
sys.path.append('..')
sys.path.append('mock')

import unittest
from mock import Mock
import simulator.relay


class TestPacket(unittest.TestCase):
    """Class for testing Relay."""

    def test_instantiation(self):
        """Test instantiation."""
        id = "test_id"
        stats = {}
        decoder = Mock(name="decoder_object")
        decoder.block_size = Mock(return_value=100)
        c = simulator.relay.Relay(id, stats, decoder)
        self.assertEqual(c.sender.id, id)
        self.assertEqual(c.receiver.id, id)
        self.assertEqual(c.receiver.decoder, decoder)

if __name__ == '__main__':
    unittest.main()
