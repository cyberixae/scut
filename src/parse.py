
from typing import Iterable
import model

def parse_pick(spec: str) -> model.Pick:
    index = int(spec)
    return model.pick([index])

def parse_concat(spec: str) -> model.Concat:
    args = spec.split('+')
    indices = [int(i) for i in args]
    return model.concat(indices, ' ')

def parse_pick_range(spec: str) -> model.PickRange:
    [arg1, arg2] = spec.split('-')
    start = len(arg1) == 0 and None or int(arg1)
    end = len(arg2) == 0 and None or int(arg2)
    return model.pick_range(start, end)

def parse_glue(spec: str) -> model.Glue:
    """
    >>> parse_glue('1-12')
    {'type': 'pick_range', 'start': 1, 'end': 12}
    """
    if '-' in spec:
        return parse_pick_range(spec)
    if '+' in spec:
        return parse_concat(spec)
    return parse_pick(spec)

def parse_glues(spec: str) -> Iterable[model.Glue]:
    return (parse_glue(glue) for glue in spec.split(','))

def parse_args(spec: str) -> Iterable[str]:
    return [spec]

def parse_chop(spec: str) -> model.Chop:
    [chop, snd] = spec.split(':')
    args = parse_args(snd)
    match chop:
        case 'split':
            return model.split(*args)
        case _:
            return model.split(*args)


def parse_blend(spec: str) -> model.Blend:
    """
    >>> parse_blend('[d: :1-12]')
    {'type': 'blend', 'chop': {'type': 'split', 'args': ' '}, 'glues': [{'type': 'pick_range', 'start': 1, 'end': 12}]}
    """
    [ch, op, glues] =  spec[1:-1].split(':')
    return model.blend(parse_chop(ch + ':' + op), *parse_glues(glues))

def parse(spec: str):
    """
    >>> parse('1-12')
    {'type': 'blend', 'chop': {'type': 'split', 'args': ' \\t\\n\\r'}, 'glues': [{'type': 'pick_range', 'start': 1, 'end': 12}]}
    """
    if spec.startswith('['):
        return parse_blend(spec)
    return model.blend(model.split(' \t\n\r'), *parse_glues(spec))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
