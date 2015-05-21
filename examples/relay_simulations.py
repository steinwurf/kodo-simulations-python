#! /usr/bin/env python
# encoding: utf-8

import sys
sys.path.append('..')

import argparse
import kodo
import simulator


def relay_simulation(symbols,
                     symbol_size,
                     error_source_sink,
                     error_source_relay,
                     error_relay_sink,
                     relay_count,
                     source_non_systematic,
                     transmit_every_tick,
                     relay_recode):
    """
    Simple relay simulation.

    The simulation has the following topology:

        .---------------------channel0-------------------.
        |                                                |
        |                    +--------+                  |
        +                    | relay0 |                  v
    +---------+              +--------+              +-------+
    | source0 |+--channel1-->          +--channel2-->| sink0 |
    +---------+              +--------+              +-------+
                             | relay1 |
                             +--------+
                                 .
                                 .
                                 .
                             +--------+
                             | relayN |
                             +--------+
    """
    encoder_factory = kodo.FullVectorEncoderFactoryBinary(symbols, symbol_size)
    decoder_factory = kodo.FullVectorDecoderFactoryBinary(symbols, symbol_size)
    s = simulator.Simulator(encoder_factory, decoder_factory)

    source = s.create_source()

    if source_non_systematic:
        source.encoder.set_systematic_off()
    else:
        source.encoder.set_systematic_on()

    sink = s.create_sink()

    channel0 = s.create_channel(error_source_sink)

    s.connect(channel0, source, sink)

    channel1 = s.create_channel(error_source_relay)
    channel2 = s.create_channel(error_relay_sink)

    for i in range(relay_count):
        relay = s.create_relay()
        relay.transmit_every_tick = transmit_every_tick
        relay.recode_on = relay_recode
        s.connect(channel1, source, relay)
        s.connect(channel2, relay, sink)

    s.run(lambda: sink.receiver.decoder.is_complete())

    return s.get_statistics()


def main():
    """Handle options and run simulation."""
    parser = argparse.ArgumentParser(
        description=relay_simulation.__doc__,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--runs",
        help="Set number of runs.",
        type=int,
        default=10000)
    parser.add_argument(
        "--symbols",
        help="Set symbols.",
        type=int,
        default=32)
    parser.add_argument(
        "--symbol-size",
        help="Set symbols size.",
        type=int,
        default=1400)
    parser.add_argument(
        "--error-source-sink",
        help="Error source to sink.",
        type=float,
        default=0.5)
    parser.add_argument(
        "--error-source-relay",
        help="Error source to relay.",
        type=float,
        default=0.5)
    parser.add_argument(
        "--error-relay-sink",
        help="Error relay to sink.",
        type=float,
        default=0.5)
    parser.add_argument(
        "--relay-count",
        help="Number of relays.",
        type=int,
        default=1)
    parser.add_argument(
        "--source-non-systematic",
        help="Whether the source is non-systematic. Systematic means that all "
             "packets in a generation are sent first once without coding. "
             "After sending everything once coding starts.",
        default=False)
    parser.add_argument(
        "--transmit-every-tick",
        help="Set true if the relay(s) should transmit in every tick or when "
             "a packet is received from the source",
        default=True)
    parser.add_argument(
        "--relay-recode",
        help="Set true if the relay(s) should recode packets",
        default=True)

    args = parser.parse_args()

    results = simulator.ResultSet()
    for run in range(args.runs):
        results.add(relay_simulation(
            args.symbols,
            args.symbol_size,
            args.error_source_sink,
            args.error_source_relay,
            args.error_relay_sink,
            args.relay_count,
            args.source_non_systematic,
            args.transmit_every_tick,
            args.relay_recode))

    print(results)

if __name__ == '__main__':
    main()
