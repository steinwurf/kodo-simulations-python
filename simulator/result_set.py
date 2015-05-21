#! /usr/bin/env python
# encoding: utf-8


class ResultSet(object):

    """ResultSet."""

    def __init__(self):
        """Initialize ResultSet."""
        super(ResultSet, self).__init__()
        self.results = []

    def add(self, result):
        """Add result."""
        self.results.append(result)

    def __iter__(self):
        """Return iterator."""
        return self.results.__iter__()

    def __len__(self):
        """Return number of results."""
        return self.results.__len__()

    def __str__(self):
        """Return string representation."""
        string = []
        for key in sorted(self.__get_keys()):
            string.append(self.__create_column(key))

        string.append("[--------]\n")
        string.append("[   DONE ]\n")
        string.append("[--------]\n")
        return "".join(string)

    def __get_keys(self):
        keys = []
        for key_list in [result.keys() for result in self.results]:
            for key in key_list:
                if key not in keys:
                    keys.append(key)
        return keys

    def __create_column(self, key):
        sum_value = 0
        count = 0
        max_value = 0
        min_value = 0

        # Collect data
        for result in self.results:
            if key not in result:
                continue
            count += 1
            r = result[key]
            sum_value += r

            max_value = r if max_value == 0 or max_value < r else max_value
            min_value = r if min_value == 0 or min_value > r else min_value

        average = float(sum_value) / count
        max_diff = max_value - average
        min_diff = min_value - average

        # Create column string
        return "".join([
            "[ RESULT ] ", key, "\n",
            "[        ]    Average: {:>6.2f} packets\n".format(average),
            "[        ]        Max: {:>6.2f} packets".format(max_value),
            " ({:>+6.2f} packets)\n".format(max_diff),
            "[        ]        Min: {:>6.2f} packets".format(min_value),
            " ({:>+6.2f} packets)\n".format(min_diff)])
