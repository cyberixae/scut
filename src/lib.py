#!/usr/bin/env python3

from typing import Callable, Iterable, TypedDict

class Split(TypedDict):
    fields: list[str]
    junk: list[str]

ChopF = Callable[[str], Split]
GlueF = Callable[[Split], Iterable[str]]
BlendF = Callable[[str], Iterable[str]]

def split(pattern: str) -> ChopF:
    """
    >>> from util import Flow
    >>> example = 'ab-12 cd-34 ab-56 cd-78'
    >>> Flow() | split(' ') < example
    {'fields': ['ab-12', 'cd-34', 'ab-56', 'cd-78'], 'junk': [' ', ' ', ' ']}
    >>> Flow() | split('- ') < example
    {'fields': ['ab', '12', 'cd', '34', 'ab', '56', 'cd', '78'], 'junk': ['-', ' ', '-', ' ', '-', ' ', '-']}
    >>> Flow() | split('ba78-') < example
    {'fields': ['', '12 cd', '34 ', '56 cd', ''], 'junk': ['ab-', '-', 'ab-', '-78']}
    """
    def _split(string: str) -> Split:
        result: Split = {
            'fields': [],
            'junk': [],
	}
        sep = False
        buf = ''
        for c in string:
            if c in pattern:
                if sep:
                    buf += c
                else:
                    result['fields'].append(buf)
                    sep = True
                    buf = c
            else:
                if sep:
                    result['junk'].append(buf)
                    sep = False
                    buf = c
                else:
                    buf += c
        if sep:
            result['junk'].append(buf)
            result['fields'].append('')
        else:
            result['fields'].append(buf)
        return result

    return _split

def pick(indices) -> GlueF:
    """
    >>> from util import Flow
    >>> Flow() | pick([4, 1, 3, 1]) | list < { 'fields': ['a', 'c', 'e', 'g'], 'junk': ['b', 'd', 'f'] }
    ['g', 'a', 'e', 'a']
    >>> Flow() | pick([1, 2, 3]) | list < { 'fields': ['a'], 'junk': ['b'] }
    ['a', '', '']
    """
    def _pick(chunks: Split):
        for i in indices:
            try:
                yield chunks['fields'][i - 1]
            except IndexError:
                yield ''
    return _pick

def pick_range(a, b) -> GlueF:
    """
    >>> from util import Flow
    >>> Flow() | pick_range(2, 3) | list < { 'fields': ['a', 'c', 'e', 'g'], 'junk': ['b', 'd', 'f'] }
    ['c', 'e']
    >>> Flow() | pick_range(2, None) | list < { 'fields': ['a', 'c', 'e', 'g'], 'junk': ['b', 'd', 'f'] }
    ['c', 'e', 'g']
    >>> Flow() | pick_range(None, 3) | list < { 'fields': ['a', 'c', 'e', 'g'], 'junk': ['b', 'd', 'f'] }
    ['a', 'c', 'e']
    >>> Flow() | pick_range(None, None) | list < { 'fields': ['a', 'c', 'e', 'g'], 'junk': ['b', 'd', 'f'] }
    ['a', 'c', 'e', 'g']
    >>> Flow() | pick_range(2, 3) | list < { 'fields': ['a', 'c'], 'junk': ['b'] }
    ['c', '']
    >>> Flow() | pick_range(1, None) | list < { 'fields': ['a', 'c'], 'junk': ['b'] }
    ['a', 'c']
    >>> Flow() | pick_range(None, 3) | list < { 'fields': ['a', 'c'], 'junk': ['b'] }
    ['a', 'c', '']
    """
    def _pick(chunks: Split):
        yield from pick(range(a or 1, (b or len(chunks['fields'])) + 1))(chunks)
    return _pick

def concat(indices: Iterable[int], delimiter: str = '') -> GlueF:
    """
    >>> from util import Flow
    >>> Flow() | concat([4, 1, 3, 1]) | list < { 'fields': ['a', 'c', 'e', 'g'], 'junk': ['b', 'd', 'f'] }
    ['gaea']
    >>> Flow() | concat([1, 2, 3]) | list < { 'fields': ['a'], 'junk': ['b'] }
    ['a']
    """
    def _concat(chunks: Split):
        return [delimiter.join(pick(indices)(chunks))]
    return _concat

def concat_range(a, b) -> GlueF:
    """
    >>> from util import Flow
    >>> Flow() | concat_range(2, 3) | list < { 'fields': ['a', 'c', 'e', 'g'], 'junk': ['b', 'd', 'f'] }
    ['ce']
    >>> Flow() | concat_range(2, None) | list < { 'fields': ['a', 'c', 'e', 'g'], 'junk': ['b', 'd', 'f'] }
    ['ceg']
    >>> Flow() | concat_range(None, 3) | list < { 'fields': ['a', 'c', 'e', 'g'], 'junk': ['b', 'd', 'f'] }
    ['ace']
    >>> Flow() | concat_range(None, None) | list < { 'fields': ['a', 'c', 'e', 'g'], 'junk': ['b', 'd', 'f'] }
    ['aceg']
    >>> Flow() | concat_range(2, 3) | list < { 'fields': ['a', 'c'], 'junk': ['b'] }
    ['c']
    >>> Flow() | concat_range(1, None) | list < { 'fields': ['a', 'c'], 'junk': ['b'] }
    ['ac']
    >>> Flow() | concat_range(None, 3) | list < { 'fields': ['a', 'c'], 'junk': ['b'] }
    ['ac']
    """
    def _concat(chunks: Split):
        return [''.join(pick_range(a, b)(chunks))]
    return _concat

def blend(chop: ChopF, *glues: GlueF) -> BlendF:
    """
    >>> from util import Flow
    >>> example = 'ab-12 cd-34 ab-56 cd-78'
    >>> Flow() | blend(split('- '), concat([2, 4]), concat([4, 2])) | list < [example]
    ['1234', '3412']
    >>> Flow() | blend(split(' '), pick([1, 3])) | blend(split('-'), pick([2])) | list < [example]
    ['12', '56']
    >>> Flow() | blend(split('-'), pick([1, 2])) | list < ['cd-34']
    ['cd', '34']
    >>> Flow() | blend(split(' '), pick([1]), Flow() | pick([2]) | blend(split('-'), pick([1, 2])) | None, pick([3, 4])) | list < [example]
    ['ab-12', 'cd', '34', 'ab-56', 'cd-78']
    """
    def _blend(strings):
        for string in strings:
            chunks = chop(string)
            for glue in glues:
                yield from glue(chunks)
    return _blend

if __name__ == "__main__":
    import doctest
    doctest.testmod()
