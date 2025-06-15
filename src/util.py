
from typing import Callable, Generic, Iterable, TypeVar, overload

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')


def identity(a: A) -> A:
    return a

def flatten(bss: Iterable[Iterable[B]]) -> Iterable[B]:
    """
    >>> flatten([['ab', 12], ['cd', 34]])
    ['ab', 12, 'cd', 34]
    """
    return [b for bs in bss for b in bs]

class Pipe(Generic[A]):
    """
    >>> Pipe(3) | (lambda x: x + 10) | (lambda x: 2 * x) | None
    26
    """
    def __init__(self, raw: A):
        self._raw = raw

    @overload
    def __or__(self, f: None) -> A: ...

    @overload
    def __or__(self, f: Callable[[A], B]) -> 'Pipe[B]': ...

    def __or__(self, f: Callable[[A], B] | None):
        if f is None:
            return self._raw
        return Pipe(f(self._raw))

class Flow(Generic[A, B]):
    """
    >>> (Flow() | (lambda x: x + 10) | (lambda x: 2 * x) | None) (3)
    26
    >>> Flow() | (lambda x: x + 10) | (lambda x: 2 * x) < 3
    26
    """
    def __init__(self, f1: Callable[[A], B] = identity) -> None:
        self._f1 = f1

    @overload
    def __or__(self, f2: None) -> Callable[[A], B]: ...

    @overload
    def __or__(self, f2: Callable[[B], C]) -> 'Flow[A, C]': ...

    def __or__(self, f2: Callable[[B], C] | None):
        if f2 is None:
            return self._f1
        def f3(raw: A) -> C:
            return f2(self._f1(raw))
        return Flow(f3)

    def __lt__(self, a: A):
        return self._f1(a)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
