#!/usr/bin/env python3

import model

def parse_glue(spec: str):
    """
    >>> parse_glue('1-12')
    {'type': 'pick_range', 'start': 1, 'end': 12}
    """
    if '-' in spec:
        [arg1, arg2] = spec.split('-')
        start = len(arg1) == 0 and None or int(arg1)
        end = len(arg2) == 0 and None or int(arg2)
        return model.pick_range(start, end)
    if '+' in spec:
        args = spec.split('+')
        indices = [int(i) for i in args]
        return model.concat(indices, ' ')
    index = int(spec)
    return model.pick(index)

def parse_blend(spec: str):
    """
    >>> parse_blend('1-12')
    {'type': 'blend', 'chop': {'type': 'split', 'args': ' \\t\\n\\r'}, 'glues': [{'type': 'pick_range', 'start': 1, 'end': 12}]}
    """
    return model.blend(model.split(' \t\n\r'), [parse_glue(glue) for glue in spec.split(',')])

def parse(spec: str):
    return parse_blend(spec)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
