#!/usr/bin/env python3

from typing import Callable, Iterable, TypedDict

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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
