
import itertools
from typing import Callable, Iterable

ChopF = Callable[[str], Iterable[str]]
GlueF = Callable[[Iterable[str]], Iterable[str]]
BlendF = Callable[[Iterable[str]], Iterable[str]]

def split_around_any_of(pattern: str) -> ChopF:
    """
    >>> from util import Flow
    >>> example = 'ab-12 cd-34 ab-56 cd-78'
    >>> Flow() | split_around_any_of(' ') | list < example
    ['ab-12', ' ', 'cd-34', ' ', 'ab-56', ' ', 'cd-78']
    >>> Flow() | split_around_any_of('- ') | list < example
    ['ab', '-', '12', ' ', 'cd', '-', '34', ' ', 'ab', '-', '56', ' ', 'cd', '-', '78']
    >>> Flow() | split_around_any_of('ba78-') | list < example
    ['', 'ab-', '12 cd', '-', '34 ', 'ab-', '56 cd', '-78', '']
    """
    def _split_around_any_of(string: str) -> Iterable[str]:
        sep = False
        buf = ''
        for c in string:
            if c in pattern:
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
        if sep:
            yield buf
            yield ''
        else:
            yield buf

    return _split_around_any_of

def _at(split: Iterable[str]) -> Iterable[str]:
        return itertools.islice(split, 0, None, 2)

def split_at_any_of(pattern: str) -> ChopF:
    """
    >>> from util import Flow
    >>> example = 'ab-12 cd-34 ab-56 cd-78'
    >>> Flow() | split_at_any_of(' ') | list < example
    ['ab-12', 'cd-34', 'ab-56', 'cd-78']
    >>> Flow() | split_at_any_of('- ') | list < example
    ['ab', '12', 'cd', '34', 'ab', '56', 'cd', '78']
    >>> Flow() | split_at_any_of('ba78-') | list < example
    ['', '12 cd', '34 ', '56 cd', '']
    """
    def _split_at_any_of(string: str) -> Iterable[str]:
        return _at(split_around_any_of(pattern)(string))

    return _split_at_any_of

def pick(indices: Iterable[int]) -> GlueF:
    """
    >>> from util import Flow
    >>> Flow() | pick([5, 4, 5, 1]) | list < ['a', 'b', 'c', 'd', 'e']
    ['e', 'd', 'e', 'a']
    >>> Flow() | pick([1, 2, 3]) | list < ['a']
    ['a', '', '']
    """
    def _pick(split: Iterable[str]) -> Iterable[str]:
        lookup = list(split)
        for i in indices:
            try:
                yield lookup[i - 1]
            except IndexError:
                yield ''
    return _pick

def pick_range(a: int | None, b: int | None) -> GlueF:
    """
    >>> from util import Flow
    >>> Flow() | pick_range(2, 3) | list < ['a', 'b', 'c', 'd']
    ['b', 'c']
    >>> Flow() | pick_range(2, None) | list < ['a', 'b', 'c', 'd']
    ['b', 'c', 'd']
    >>> Flow() | pick_range(None, 3) | list < ['a', 'b', 'c', 'd']
    ['a', 'b', 'c']
    >>> Flow() | pick_range(None, None) | list < ['a', 'b', 'c', 'd']
    ['a', 'b', 'c', 'd']
    >>> Flow() | pick_range(2, 3) | list < ['a', 'b']
    ['b', '']
    >>> Flow() | pick_range(1, None) | list < ['a', 'b']
    ['a', 'b']
    >>> Flow() | pick_range(None, 3) | list < ['a', 'b']
    ['a', 'b', '']
    """
    def _pick(split: Iterable[str]) -> Iterable[str]:
        lookup = list(split)
        first = a or 1
        last = b or len(lookup)
        yield from pick(range(first, last + 1))(lookup)
    return _pick

def concat(indices: Iterable[int], delimiter: str = '') -> GlueF:
    """
    >>> from util import Flow
    >>> Flow() | concat([5, 4, 5, 1]) | list < ['a', 'b', 'c', 'd', 'e']
    ['edea']
    >>> Flow() | concat([1, 2, 3]) | list < ['a']
    ['a']
    """
    def _concat(split: Iterable[str]):
        return [delimiter.join(pick(indices)(split))]
    return _concat

def concat_range(a: int | None, b: int | None) -> GlueF:
    """
    >>> from util import Flow
    >>> Flow() | concat_range(2, 3) | list < ['a', 'b', 'c', 'd']
    ['bc']
    >>> Flow() | concat_range(2, None) | list < ['a', 'b', 'c', 'd']
    ['bcd']
    >>> Flow() | concat_range(None, 3) | list < ['a', 'b', 'c', 'd']
    ['abc']
    >>> Flow() | concat_range(None, None) | list < ['a', 'b', 'c', 'd']
    ['abcd']
    >>> Flow() | concat_range(2, 3) | list < ['a', 'b']
    ['b']
    >>> Flow() | concat_range(1, None) | list < ['a', 'b']
    ['ab']
    >>> Flow() | concat_range(None, 3) | list < ['a', 'b']
    ['ab']
    """
    def _concat(split: Iterable[str]):
        return [''.join(pick_range(a, b)(split))]
    return _concat

def blend(chop: ChopF, *glues: GlueF) -> BlendF:
    """
    >>> from util import Flow
    >>> example = 'ab-12 cd-34 ab-56 cd-78'
    >>> Flow() | blend(split_at_any_of('- '), concat([2, 4]), concat([4, 2])) | list < [example]
    ['1234', '3412']
    >>> Flow() | blend(split_at_any_of(' '), pick([1, 3])) | blend(split_at_any_of('-'), pick([2])) | list < [example]
    ['12', '56']
    >>> Flow() | blend(split_at_any_of('-'), pick([1, 2])) | list < ['cd-34']
    ['cd', '34']
    >>> Flow() | blend(split_at_any_of(' '), pick([1]), Flow() | pick([2]) | blend(split_at_any_of('-'), pick([1, 2])) | None, pick([3, 4])) | list < [example]
    ['ab-12', 'cd', '34', 'ab-56', 'cd-78']
    """
    def _blend(strings: Iterable[str]) -> Iterable[str]:
        for string in strings:
            split = list(chop(string))
            for glue in glues:
                yield from glue(split)
    return _blend

if __name__ == "__main__":
    import doctest
    doctest.testmod()
