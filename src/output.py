
import csv
import json
import string
from typing import Iterable, List, TextIO

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

def output_csv_no_head(output: TextIO):
    """
    >>> import io
    >>> buffer = io.StringIO()
    >>> output_csv_no_head(buffer)([[12, 34], [56, 78]])
    >>> dos = buffer.getvalue()
    >>> unix = dos.replace('\\r\\n', '\\n')
    >>> print(unix)
    12,34
    56,78
    <BLANKLINE>
    """
    def _csv(rows: Iterable[Iterable[str]]):
        w = csv.writer(output)
        for row in rows:
            w.writerow(row)
    return _csv

def output_csv_gen_head(output: TextIO):
    """
    >>> import io
    >>> buffer = io.StringIO()
    >>> output_csv_gen_head(buffer)([[12, 34], [56, 78]])
    >>> dos = buffer.getvalue()
    >>> unix = dos.replace('\\r\\n', '\\n')
    >>> print(unix)
    a,b
    12,34
    56,78
    <BLANKLINE>
    """
    def _csv(iterator: Iterable[Iterable[str]]):
        rows = [list(row) for row in iterator]
        head = head_from_rows(rows)
        lines = (head, *rows)
        output_csv_no_head(output)(lines)
    return _csv

def output_json(output: TextIO):
    """
    >>> import io
    >>> buffer = io.StringIO()
    >>> output_json(buffer)([[12, 34], [56, 78]])
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
        output.write(indent * '  ' + payload + le)

    def _json(rows: Iterable[Iterable[str]]):
        lehe = 0
        first = True
        write(0, '{')
        write(1, '"rows": [')
        for iterator in rows:
            if first:
                first = False
            else:
                write(0, ',')
            row = list(iterator)
            lehe = max(lehe, len(row))
            write(2, json.dumps(row), '')
        write(0)
        write(1, '],')
        write(1, '"header": ' + json.dumps(head_from_len(lehe)))
        write(0, '}')
    return _json

if __name__ == "__main__":
    import doctest
    doctest.testmod()
