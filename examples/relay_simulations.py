#! /usr/bin/env python
# encoding: utf-8

import sys
sys.path.append('..')

import argparse
import kodo
import simulator
import collections


def relay_simulation(symbols,
                     symbol_size,
                     error_source_sink,
                     error_source_relay,
                     error_relay_sink,
                     relay_count,
                     source_systematic,
                     relay_transmit_on_receive,
                     relay_recode):
    """
    Simple relay simulation.


    The simulation has the following topology:

        .-----------------------------.
        |                             |
        |           +-------+         |
        +           | relay |         v
    +--------+      +-------+     +------+
    | source | +-->           +-> | sink |
    +--------+      +-------+     +------+
                    | relay |
                    +-------+
                        .
                        .
                        .
                    +-------+
                    | relay |
                    +-------+
    """
    nodes = []

    # Create source
    encoder_factory = kodo.FullVectorEncoderFactoryBinary(symbols, symbol_size)
    encoder = encoder_factory.build()

    if source_systematic:
        encoder.set_systematic_on()
    else:
        encoder.set_systematic_off()

    source = simulator.Source("source0", encoder)
    nodes.append(source)

    # Create sink
    decoder_factory = kodo.FullVectorDecoderFactoryBinary(symbols, symbol_size)
    sink = simulator.Sink("sink0", decoder_factory.build())
    nodes.append(sink)

    # Create channels
    source_sink = simulator.Channel("channel0", error_source_sink)
    nodes.append(source_sink)
    source_relay = simulator.Channel("channel1", error_source_relay)
    nodes.append(source_relay)
    relay_sink = simulator.Channel("channel2", error_relay_sink)
    nodes.append(relay_sink)

    # Connect source and sink
    source.receivers.append(source_sink)
    source_sink.receivers.append(sink)

    relays = []
    for i in range(relay_count):
        # Create relay
        relay_id = "relay{}".format(i)
        relay = simulator.Relay(relay_id, decoder_factory.build())
        relay.transmit_on_receive = relay_transmit_on_receive
        relay.recode = relay_recode

        relays.append(relay)
        nodes.append(relay)

        # Connect source and relay
        source.receivers.append(source_relay)
        source_relay.receivers.append(relay)

        # Connect source and relay
        relay.receivers.append(relay_sink)
        relay_sink.receivers.append(sink)

    while not sink.decoder.is_complete():
        source.tick()
        for relay in relays:
            relay.tick()

    result = {}
    for node in nodes:
        result.update(node.counter)
    return result


def print_column(key, results):
    """Print column of data nicely."""
    sum_value = 0
    count = 0
    max_value = 0
    min_value = 0

    for result in results:
        if key not in result:
            continue
        count += 1
        r = result[key]
        sum_value += r
        max_value = r if max_value == 0 or max_value < r else max_value
        min_value = r if min_value == 0 or min_value > r else min_value

    average = float(sum_value) / count

    print(
        "[   RESULT ] {key}\n"
        "[          ]    Average: {average} packets\n"
        "[          ]        Max: {max} packets ({max_diff} packets)\n"
        "[          ]        Max: {min} packets ({min_diff} packets)\n"
        "[          ]".format(
                key=key,
                average=average,
                max=max_value,
                max_diff=max_value - average,
                min=min_value,
                min_diff=min_value - average))


def present_results(results):
    """Print out results nicely."""
    def get_keys(results):
        keys = []
        for key_list in [result.keys() for result in results]:
            for key in key_list:
                if key not in keys:
                    keys.append(key)
        return keys

    for key in sorted(get_keys(results)):
        print_column(key, results)
    print("[----------]\n"
          "[     DONE ]\n"
          "[----------]")


def main():
    """Handle options and run simulation."""
    parser = argparse.ArgumentParser(description="relay line")
    parser.add_argument(
        "--symbols",
        help="Set symbols",
        type=int,
        default=32)
    parser.add_argument(
        "--symbol-size",
        help="Set symbols size",
        type=int,
        default=1400)
    parser.add_argument(
        "--error-source-sink",
        help="Error source to sink",
        type=float,
        default=0.5)
    parser.add_argument(
        "--error-source-relay",
        help="Error source to relay",
        type=float,
        default=0.5)
    parser.add_argument(
        "--error-relay-sink",
        help="Error relay to sink",
        type=float,
        default=0.5)
    parser.add_argument(
        "--relay-count",
        help="Number of relays",
        type=int,
        default=1)
    parser.add_argument(
        "--source-systematic",
        help="Whether the source is systematic or not --systematic=1 turns on "
             "systematic source. Systematic means that all packets in a "
             "generation are sent first once without coding. After sending "
             "everything once coding starts",
        default=True)
    parser.add_argument(
        "--relay-transmit-on-receive",
        help="Set true if the relay(s) should transmit in every tick or when "
             "a packet is received from the source",
        default=True)
    parser.add_argument(
        "--relay-recode",
        help="Set true if the relay(s) should recode packets",
        default=True)

    args = parser.parse_args()

    runs = 100
    results = []
    for run in range(runs):
        result = relay_simulation(
            args.symbols,
            args.symbol_size,
            args.error_source_sink,
            args.error_source_relay,
            args.error_relay_sink,
            args.relay_count,
            args.source_systematic,
            args.relay_transmit_on_receive,
            args.relay_recode)
        results.append(result)

    present_results(results)


if __name__ == '__main__':
    main()
