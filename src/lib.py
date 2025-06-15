#!/usr/bin/env python3

from typing import Iterable, TypedDict

def identity(x):
    return x

def flatten(xss):
    """
    >>> flatten([['ab', 12], ['cd', 34]])
    ['ab', 12, 'cd', 34]
    """
    return [x for xs in xss for x in xs]

class Pipe:
    """
    >>> Pipe(3) | (lambda x: x + 10) | (lambda x: 2 * x) | None
    26
    """
    def __init__(self, raw):
        self._raw = raw

    def __or__(self, f):
        if f is None:
            return self._raw
        return Pipe(f(self._raw))

class Flow:
    """
    >>> (Flow() | (lambda x: x + 10) | (lambda x: 2 * x) | None) (3)
    26
    >>> Flow() | (lambda x: x + 10) | (lambda x: 2 * x) < 3
    26
    """
    def __init__(self, f1=identity):
        self._f1 = f1

    def __or__(self, f2):
        if f2 is None:
            return self._f1
        def f3(raw):
            return f2(self._f1(raw))
        return Flow(f3)

    def __lt__(self, x):
        return self._f1(x)

class Split(TypedDict):
    pattern: str
    fields: list[str]
    junk: list[str]

def split(pattern: str):
    """
    >>> example = 'ab-12 cd-34 ab-56 cd-78'
    >>> Flow() | split(' ') < example
    {'pattern': ' ', 'fields': ['ab-12', 'cd-34', 'ab-56', 'cd-78'], 'junk': [' ', ' ', ' ']}
    >>> Flow() | split('- ') < example
    {'pattern': '- ', 'fields': ['ab', '12', 'cd', '34', 'ab', '56', 'cd', '78'], 'junk': ['-', ' ', '-', ' ', '-', ' ', '-']}
    >>> Flow() | split('ba78-') < example
    {'pattern': 'ba78-', 'fields': ['', '12 cd', '34 ', '56 cd', ''], 'junk': ['ab-', '-', 'ab-', '-78']}
    """
    def _split(string: str) -> Split:
        result: Split = {
            'pattern': pattern,
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

def pick(indices):
    """
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

def pick_range(a, b):
    """
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

def concat(indices: Iterable[int], delimiter: str = ''):
    """
    >>> Flow() | concat([4, 1, 3, 1]) | list < { 'fields': ['a', 'c', 'e', 'g'], 'junk': ['b', 'd', 'f'] }
    ['gaea']
    >>> Flow() | concat([1, 2, 3]) | list < { 'fields': ['a'], 'junk': ['b'] }
    ['a']
    """
    def _concat(chunks: Split):
        return [delimiter.join(pick(indices)(chunks))]
    return _concat

def concat_range(a, b):
    """
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

def blend(chop, *glues):
    """
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
