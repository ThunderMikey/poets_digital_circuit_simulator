#!/usr/bin/env python3
# Compare simulation results from
# * POETS
# * Verilator

import argparse
import re

class RejectingDict(dict):
    def __setitem__(self, k, v):
        try:
            self.__getitem__(k)
            print(self)
            raise ValueError("Key: {} is already present".format(k))
        except KeyError:
            return super(RejectingDict, self).__setitem__(k, v)

def compare(poetsResultFile, verilatorResultFile):

    poetsResults = RejectingDict()
    verilatorResults = RejectingDict()

    poetsResultMatcher = re.compile('io_oracle.+ print : feedin: (?P<feedin>\d+), result: (?P<result>\d+)')
    verilatorResultMatcher = re.compile('input: (?P<feedin>\d+), output: (?P<result>\d+)')



    with open(poetsResultFile) as pr:
        for line in pr:
            m = poetsResultMatcher.search(line)
            if m is not None:
                assert(len(m.groups()) == 2)
                feedinValue = m.group('feedin')
                resultValue = m.group('result')
                try:
                    intFeedinValue = int(feedinValue)
                except ValueError:
                    raise("{} is not an integer!".format(feedinValue))
                try:
                    intResultValue = int(resultValue)
                except ValueError:
                    raise("{} is not an integer!".format(resultValue))
                poetsResults[intFeedinValue] = intResultValue

    with open(verilatorResultFile) as pr:
        for line in pr:
            m = verilatorResultMatcher.search(line)
            if m is not None:
                assert(len(m.groups()) == 2)
                feedinValue = m.group('feedin')
                resultValue = m.group('result')
                try:
                    intFeedinValue = int(feedinValue)
                except ValueError:
                    raise("{} is not an integer!".format(feedinValue))
                try:
                    intResultValue = int(resultValue)
                except ValueError:
                    raise("{} is not an integer!".format(resultValue))
                verilatorResults[intFeedinValue] = intResultValue

    if poetsResults == verilatorResults:
        # all good
        pass
    else:
        print(set(poetsResults.items())^
                set(verilatorResults.items()))
        raise(RuntimeError("Results does not match!"))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="simulation results comparitor.")

    parser.add_argument('-p', '--poets', dest='poets_result',
            type=str, required=True, action='store',
            help="POETS simulation result file")
    parser.add_argument('-v', '--verilator', dest='verilator_result',
            type=str, required=True, action='store',
            help="Verilator simualtion result file")

    args = parser.parse_args()
    poetsResultFile = args.poets_result
    verilatorResultFile = args.verilator_result
    compare(poetsResultFile, verilatorResultFile)
