#!/usr/bin/env python3

import sys

import output
import process
from util import Flow

def run(spec: str):
    return Flow() | process.process(spec) | output.output_csv_gen_head(sys.stdout) < sys.stdin

def main(args):
    if len(args) < 2:
      print('nothing to do')
      return
    arg = args[1]
    run(arg)

if __name__ == "__main__":
    main(sys.argv)