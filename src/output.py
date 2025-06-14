#!/usr/bin/env python3

import csv
import json
import string
from typing import Iterator, List, TextIO

def head_from_len(row_len: int):
    """
    >>> head_from_len(3)
    ['a', 'b', 'c']
    """
    return list(string.ascii_lowercase[:row_len])

def head_from_rows(rows: List[List[str]]):
    """
    >>> head_from_rows([[1, 2], [3, 4, 5], [], [6, 7]])
    ['a', 'b', 'c']
    """
    row_len = max(len(row) for row in rows)
    return head_from_len(row_len)

def output_csv_no_head(rows: Iterator[List[str]], output: TextIO):
    """
    >>> import io
    >>> buffer = io.StringIO()
    >>> output_csv_no_head([[12, 34], [56, 78]], buffer)
    >>> dos = buffer.getvalue()
    >>> unix = dos.replace('\\r\\n', '\\n')
    >>> print(unix)
    12,34
    56,78
    <BLANKLINE>
    """
    w = csv.writer(output)
    for row in rows:
        w.writerow(row)

def output_csv_gen_head(iterator: Iterator[List[str]], output: TextIO):
    """
    >>> import io
    >>> buffer = io.StringIO()
    >>> output_csv_gen_head([[12, 34], [56, 78]], buffer)
    >>> dos = buffer.getvalue()
    >>> unix = dos.replace('\\r\\n', '\\n')
    >>> print(unix)
    a,b
    12,34
    56,78
    <BLANKLINE>
    """
    rows = list(iterator)
    head = head_from_rows(rows)
    lines = iter((head, *rows))
    output_csv_no_head(lines, output)

def output_json(rows: Iterator[List[str]], output: TextIO):
    """
    >>> import io
    >>> buffer = io.StringIO()
    >>> output_json([[12, 34], [56, 78]], buffer)
    >>> print(buffer.getvalue())
    {
      "rows": [
        [12, 34],
        [56, 78]
      ],
      "header": ["a", "b"]
    }
    <BLANKLINE>
    """
    def write(indent, payload='', le='\n'):
        output.write(indent * '  ' + payload + le )

    lehe = 0
    first = True
    write(0, '{')
    write(1, '"rows": [')
    for row in rows:
        if first:
            first = False
        else:
            write(0, ',')
        lehe = max(lehe, len(row))
        write(2, json.dumps(row), '')
    write(0)
    write(1, '],')
    write(1, '"header": ' + json.dumps(head_from_len(lehe)))
    write(0, '}')

if __name__ == "__main__":
    import doctest
    doctest.testmod()
