#!/usr/bin/env python3
# Compare simulation results from
# * POETS
# * Verilator

import argparse
import re
from os import listdir
from os.path import isfile, join
from compare_poets_verilator_results import compare

parser = argparse.ArgumentParser(description="simulation results comparitor for directories of them.")

parser.add_argument('-p', '--poets_dir', dest='poets_dir',
        type=str, required=True, action='store',
        help="POETS simulation result file directory")
parser.add_argument('-v', '--verilator_dir', dest='verilator_dir',
        type=str, required=True, action='store',
        help="Verilator simulation result file directory")

args = parser.parse_args()

poets_dir = args.poets_dir
verilator_dir = args.verilator_dir

# comparison is based on files in poets_dir
poets_logs = listdir(poets_dir)
verilator_logs = listdir(verilator_dir)

assert set(poets_logs).issubset(set(verilator_logs)), "Verilator logs dir does not contain everything in POETS logs."

if __name__ == "__main__":
    for poets_log in poets_logs:
        pl = join(poets_dir, poets_log)
        vl = join(verilator_dir, poets_log)
        try:
            compare(poetsResultFile=pl, verilatorResultFile=vl)
        except Exception as e:
            print(e.__doc__)
            raise(RuntimeError("{} has gone wrong".format(poets_log)))
