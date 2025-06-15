#!/usr/bin/env python3

from typing import List

def pick(index: int):
    return { 'type': 'pick', 'index': index }

def concat(indices: List[int], delimiter):
    return { 'type': 'concat', 'indices': indices, 'delimiter': delimiter}

def pick_range(start: int | None, end: int | None):
    return { 'type': 'pick_range', 'start': start, 'end': end }

def concat_range(start: int | None, end: int | None):
    return { 'type': 'concat_range', 'start': start, 'end': end }

def split(args):
    return { 'type': 'split', 'args': args }

def blend(chop, glues):
    return { 'type': 'blend', 'chop': chop, 'glues': glues }

if __name__ == "__main__":
    import doctest
    doctest.testmod()
