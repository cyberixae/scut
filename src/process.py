#!/usr/bin/env python3

import lib
import parse

def process_glue(glue):
    match glue['type']:
        case 'pick':
            return lib.pick(glue['index'])
        case 'pick_range':
            return lib.pick_range(glue['start'], glue['end'])
        case 'concat':
            return lib.concat(glue['indices'], glue['delimiter'])
        case 'concat_range':
            return lib.pick_range(glue['start'], glue['end'])

def process_chop(chop):
    match chop['type']:
        case 'split':
            return lib.split(' \t\n\r')

def process_blend(blend):
    """
    >>> lib.Flow() | process_blend({ 'type': 'blend', 'chop': { 'type': 'split', 'args': ' \\t\\n\\r' }, 'glues': [{ 'type': 'pick_range', 'start': 1, 'end': 12 }] }) | list < ["lrwxr-xr-- 1 user group    123 May 25 16:24 'cpu info' -> /proc/cpuinfo"]
    ['lrwxr-xr--', '1', 'user', 'group', '123', 'May', '25', '16:24', "'cpu", "info'", '->', '/proc/cpuinfo']
    """
    return lib.blend(process_chop(blend['chop']), *(process_glue(glue) for glue in blend['glues']))

def process(spec: str):
    """
    >>> lib.Flow() | process('1-12') | list < ["lrwxr-xr-- 1 user group    123 May 25 16:24 'cpu info' -> /proc/cpuinfo"]
    ['lrwxr-xr--', '1', 'user', 'group', '123', 'May', '25', '16:24', "'cpu", "info'", '->', '/proc/cpuinfo']
    >>> lib.Flow() | process('1-5,6+7+8,9-12') | list < ["lrwxr-xr-- 1 user group    123 May 25 16:24 'cpu info' -> /proc/cpuinfo"]
    ['lrwxr-xr--', '1', 'user', 'group', '123', 'May 25 16:24', "'cpu", "info'", '->', '/proc/cpuinfo']
    """
    return process_blend(parse.parse(spec))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
