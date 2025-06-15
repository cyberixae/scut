
import sys
from typing import Iterable
import lib
from model import Blend, Chop, Concat, ConcatRange, Glue, Pick, PickRange, Split
import parse

def process_split(split: Split) -> lib.ChopF:
    """
    >>> from util import Flow
    >>> import model
    >>> Flow() | process_split(model.split(' \\t\\n\\r')) < "lrwxr-xr-- 1 user group    123 May 25 16:24 'cpu info' -> /proc/cpuinfo"
    {'fields': ['lrwxr-xr--', '1', 'user', 'group', '123', 'May', '25', '16:24', "'cpu", "info'", '->', '/proc/cpuinfo'], 'junk': [' ', ' ', ' ', '    ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']}
    """
    return lib.split(split['args'])

def process_chop(chop: Chop) -> lib.ChopF:
    """
    >>> from util import Flow
    >>> import model
    >>> Flow() | process_chop(model.split(' \\t\\n\\r')) < "lrwxr-xr-- 1 user group    123 May 25 16:24 'cpu info' -> /proc/cpuinfo"
    {'fields': ['lrwxr-xr--', '1', 'user', 'group', '123', 'May', '25', '16:24', "'cpu", "info'", '->', '/proc/cpuinfo'], 'junk': [' ', ' ', ' ', '    ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']}
    """
    match chop['type']:
        case 'split':
            return process_split(chop)

def process_pick(pick: Pick) -> lib.GlueF:
    return lib.pick(pick['index'])

def process_concat(concat: Concat) -> lib.GlueF:
    return lib.concat(concat['indices'], concat['delimiter'])

def process_pick_range(pick_range: PickRange) -> lib.GlueF:
    return lib.pick_range(pick_range['start'], pick_range['end'])

def process_concat_range(concat_range: ConcatRange) -> lib.GlueF:
    return lib.pick_range(concat_range['start'], concat_range['end'])

def process_glue(glue: Glue) -> lib.GlueF:
    match glue['type']:
        case 'pick':
            return process_pick(glue)
        case 'pick_range':
            return process_pick_range(glue)
        case 'concat':
            return process_concat(glue)
        case 'concat_range':
            return process_concat_range(glue)

def process_glues(glues: Iterable[Glue]) -> Iterable[lib.GlueF]:
    return (process_glue(glue) for glue in glues)

def process_blend(blend: Blend) -> lib.BlendF:
    """
    >>> from util import Flow
    >>> import model
    >>> Flow() | process_blend(model.blend(model.split(' \\t\\n\\r'), model.pick_range(1, 12))) | list < ["lrwxr-xr-- 1 user group    123 May 25 16:24 'cpu info' -> /proc/cpuinfo"]
    ['lrwxr-xr--', '1', 'user', 'group', '123', 'May', '25', '16:24', "'cpu", "info'", '->', '/proc/cpuinfo']
    """
    return lib.blend(process_chop(blend['chop']), *process_glues(blend['glues']))

def process(spec: str):
    """
    >>> from util import Flow
    >>> Flow() | process('1-12') | list < ["lrwxr-xr-- 1 user group    123 May 25 16:24 'cpu info' -> /proc/cpuinfo"]
    ['lrwxr-xr--', '1', 'user', 'group', '123', 'May', '25', '16:24', "'cpu", "info'", '->', '/proc/cpuinfo']
    >>> Flow() | process('1-5,6+7+8,9-12') | list < ["lrwxr-xr-- 1 user group    123 May 25 16:24 'cpu info' -> /proc/cpuinfo"]
    ['lrwxr-xr--', '1', 'user', 'group', '123', 'May 25 16:24', "'cpu", "info'", '->', '/proc/cpuinfo']
    """
    return process_blend(parse.parse(spec))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
