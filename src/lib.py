#!/usr/bin/env python3

class Pipe:
    """
    >>> Pipe(3) | (lambda x: 2 * x) | None
    6
    """
    def __init__(self, raw):
        self._raw = raw

    def __or__(self, f):
        if f is None:
            return self._raw
        return Pipe(f(self._raw))

def flatten(xss):
    """
    >>> flatten([['ab', 12], ['cd', 34]])
    ['ab', 12, 'cd', 34]
    """
    return [x for xs in xss for x in xs]

def split(chars):
    """
    >>> example = 'ab-12 cd-34 ab-56 cd-78'
    >>> Pipe(example) | split(' ') | list | None
    ['ab-12', ' ', 'cd-34', ' ', 'ab-56', ' ', 'cd-78']
    >>> Pipe(example) | split('- ') | list | None
    ['ab', '-', '12', ' ', 'cd', '-', '34', ' ', 'ab', '-', '56', ' ', 'cd', '-', '78']
    >>> Pipe(example) | split('ba78-') | list | None
    ['', 'ab-', '12 cd', '-', '34 ', 'ab-', '56 cd', '-78', '']
    """
    def _split(string):
        sep = False
        buf = ''
        for c in string:
            if c in chars:
                if sep:
                    buf += c
                else:
                    yield buf
                    sep = True
                    buf = c
            else:
                if sep:
                    yield buf
                    sep = False
                    buf = c
                else:
                    buf += c
        yield buf
        if sep:
          yield ''
    return _split

def pick(indices):
    """
    >>> Pipe('abcdefg') | pick([1, 2, 3]) | list | None
    ['a', 'c', 'e']
    >>> Pipe('ab') | pick([1, 2, 3]) | list | None
    ['a', '', '']
    """
    def _pick(chunks):
        for i in indices:
            try:
                yield chunks[(i - 1) * 2]
            except IndexError:
                yield ''
    return _pick

def concat(indices):
    """
    >>> Pipe('abcdefg') | concat([1, 2, 3]) | list | None
    ['ace']
    >>> Pipe('ab') | concat([1, 2, 3]) | list | None
    ['a']
    """
    def _concat(chunks):
        return [''.join(pick(indices)(chunks))]
    return _concat

def blend(chop, *glues):
    """
    >>> example = 'ab-12 cd-34 ab-56 cd-78'
    >>> Pipe([example]) | blend(split('- '), concat([2, 4]), concat([4, 2])) | list | None
    ['1234', '3412']
    >>> Pipe([example]) | blend(split(' '), pick([1, 3])) | blend(split('-'), pick([2])) | list | None
    ['12', '56']
    """
    def _blend(strings):
        for string in strings:
            chunks = list(chop(string))
            for glue in glues:
                yield from glue(chunks)
    return _blend

if __name__ == "__main__":
    import doctest
    doctest.testmod()
