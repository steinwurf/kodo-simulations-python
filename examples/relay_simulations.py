#! /usr/bin/env python
# encoding: utf-8

import sys
sys.path.append('..')

import argparse
import kodo
import simulator


def print_setup(runs,
                symbols,
                symbol_size,
                error_source_sink,
                error_source_relay,
                error_relay_sink,
                relay_count,
                source_systematic,
                transmit_every_tick,
                relay_recode):
    """Print the setup."""
    print("[--------]")
    print("[ SETUP  ] configuration.simulation")
    print("[        ]   Runs: {} runs".format(runs))
    print("[ SETUP  ] configuration.coding")
    print("[        ]        Relay Recode: {}".format(relay_recode))
    print("[        ]     Size of Symbols: {} bytes".format(symbol_size))
    print("[        ]   Number of Symbols: {} symbols".format(symbols))
    print("[        ]   Source Systematic: {}".format(source_systematic))
    print("[ SETUP  ] configuration.network")
    print("[        ]             Relay Count: {} relays".format(relay_count))
    print("[        ]     Relay To Sink Error: {}".format(error_relay_sink))
    print("[        ]     Transmit Every Tick: {}".format(transmit_every_tick))
    print("[        ]    Source To Sink Error: {}".format(error_source_sink))
    print("[        ]   Source To Relay Error: {}".format(error_source_relay))
    print("[--------]")


def relay_simulation(symbols,
                     symbol_size,
                     error_source_sink,
                     error_source_relay,
                     error_relay_sink,
                     relay_count,
                     source_systematic,
                     transmit_every_tick,
                     relay_recode):
    """
    Simple relay simulator.

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

    if source_systematic:
        source.encoder.set_systematic_on()
    else:
        source.encoder.set_systematic_off()

    sink = s.create_sink()

    channel0 = s.create_channel(channel_condition=error_source_sink)

    s.connect(channel=channel0, a=source, b=sink)

    channel1 = s.create_channel(channel_condition=error_source_relay)
    channel2 = s.create_channel(channel_condition=error_relay_sink)

    for i in range(relay_count):
        relay = s.create_relay()
        relay.transmit_every_tick = transmit_every_tick
        relay.recode_on = relay_recode
        s.connect(channel=channel1, a=source, b=relay)
        s.connect(channel=channel2, a=relay, b=sink)

    s.run(done=lambda: sink.receiver.finished())

    return s.get_statistics()


def main():
    """Handle options and run simulator."""
    parser = argparse.ArgumentParser(
        description=relay_simulation.__doc__,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--runs",
        help="Set number of runs.",
        type=int,
        default=100)
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
        "--source-systematic",
        help="Whether the source is systematic. Systematic means that all "
             "packets in a generation are sent first once without coding. "
             "After sending everything once coding starts.",
        default=True)
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

    print_setup(
        runs=args.runs,
        symbols=args.symbols,
        symbol_size=args.symbol_size,
        error_source_sink=args.error_source_sink,
        error_source_relay=args.error_source_relay,
        error_relay_sink=args.error_relay_sink,
        relay_count=args.relay_count,
        source_systematic=args.source_systematic,
        transmit_every_tick=args.transmit_every_tick,
        relay_recode=args.relay_recode)

    results = simulator.ResultSet()
    for run in range(args.runs):
        results.add(relay_simulation(
            symbols=args.symbols,
            symbol_size=args.symbol_size,
            error_source_sink=args.error_source_sink,
            error_source_relay=args.error_source_relay,
            error_relay_sink=args.error_relay_sink,
            relay_count=args.relay_count,
            source_systematic=args.source_systematic,
            transmit_every_tick=args.transmit_every_tick,
            relay_recode=args.relay_recode))

    print(results)

if __name__ == '__main__':
    main()
