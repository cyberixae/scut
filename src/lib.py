#!/usr/bin/env python3

"""
>>> example = 'ab-12 cd-34 ab-56 cd-78'
>>> list(chop(' ', example))
['ab-12', ' ', 'cd-34', ' ', 'ab-56', ' ', 'cd-78']
>>> list(chop('- ', example))
['ab', '-', '12', ' ', 'cd', '-', '34', ' ', 'ab', '-', '56', ' ', 'cd', '-', '78']
>>> list(chop('ba78-', example))
['ab-', '12 cd', '-', '34 ', 'ab-', '56 cd', '-78']
>>> list(split(' ', example))
['ab-12', 'cd-34', 'ab-56', 'cd-78']
>>> list(split('- ', example))
['ab', '12', 'cd', '34', 'ab', '56', 'cd', '78']
>>> list(split('ba78-', example))
['', '12 cd', '34 ', '56 cd', '']
>>> list(match(' ', example))
[' ', ' ', ' ']
>>> list(match('- ', example))
['-', ' ', '-', ' ', '-', ' ', '-']
>>> list(match('ba78-', example))
['ab-', '-', 'ab-', '-78']
"""

import string

def chop(chars, line):
    sep = None
    buf = ''
    for i in range(len(line)):
        c = line[i]
        if c in chars:
            if sep == None:
               sep = True
            if sep:
                buf += c
            else:
                yield buf
                sep = True
                buf = c
        else:
            if sep == None:
               sep = False
            if sep:
                yield buf
                sep = False
                buf = c
            else:
                buf += c
    yield buf

def split(chars, line):
    out = True
    for part in chop(chars, line):
        if out:
            yield part
        out = not(out)

def match(chars, line):
    out = False
    for part in chop(chars, line):
        if out:
            yield part
        out = not(out)

    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
