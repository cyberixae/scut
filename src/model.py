
from typing import List, Literal, TypedDict

class Pick(TypedDict):
    type: Literal['pick']
    index: int

def pick(index: int) -> Pick:
    return { 'type': 'pick', 'index': index }

class Concat(TypedDict):
    type: Literal['concat']
    indices: List[int]
    delimiter: str

def concat(indices: List[int], delimiter) -> Concat:
    return { 'type': 'concat', 'indices': indices, 'delimiter': delimiter}

class PickRange(TypedDict):
    type: Literal['pick_range']
    start: int | None
    end: int | None

def pick_range(start: int | None, end: int | None) -> PickRange:
    return { 'type': 'pick_range', 'start': start, 'end': end }

class ConcatRange(TypedDict):
    type: Literal['concat_range']
    start: int | None
    end: int | None

def concat_range(start: int | None, end: int | None) -> ConcatRange:
    return { 'type': 'concat_range', 'start': start, 'end': end }

Glue = Pick | Concat | PickRange | ConcatRange

class Split(TypedDict):
    type: Literal['split']
    args: str

def split(args) -> Split:
    return { 'type': 'split', 'args': args }

Chop = Split

class Blend(TypedDict):
    type: Literal['blend']
    chop: Chop
    glues: List[Glue]

def blend(chop: Chop, *glues: Glue) -> Blend:
    return { 'type': 'blend', 'chop': chop, 'glues': list(glues) }

if __name__ == "__main__":
    import doctest
    doctest.testmod()
