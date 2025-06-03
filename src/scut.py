#!/usr/bin/env python3

import csv
import sys
import string

import lib

def minus(m):
    """
    >>> list(minus('1-3'))
    ['1', '2', '3']
    """
    parts = m.split('-')
    if len(parts) == 1:
        return parts
    if len(parts) == 2:
        [s, e] = parts
        return (str(i) for i in range(int(s or '1'), int(e or '1') + 1))

def parse(spec_string):
    return lib.flatten([minus(i) for i in spec_string.split(',')])

def build(speced, line):
    parts = list(lib.split([' ','\t','\n','\r'])(line))
    def get(i):
        try:
            return parts[i]
        except:
            return ''
    glued = [' '.join([get((int(x)-1)*2) for x in p.split('+')]) for p in speced]
    return glued

def test(spec, line):
    """
    >>> test('1-12', "lrwxr-xr-- 1 user group    123 May 25 16:24 'cpu info' -> /proc/cpuinfo")
    ['lrwxr-xr--', '1', 'user', 'group', '123', 'May', '25', '16:24', "'cpu", "info'", '->', '/proc/cpuinfo']
    >>> test('1-5,6+7+8,9-12', "lrwxr-xr-- 1 user group    123 May 25 16:24 'cpu info' -> /proc/cpuinfo")
    ['lrwxr-xr--', '1', 'user', 'group', '123', 'May 25 16:24', "'cpu", "info'", '->', '/proc/cpuinfo']
    """
    return build(parse(spec), line)

def run(spec):
    speced = parse(spec)
    lehe = len(speced)
    w = csv.writer(sys.stdout)
    w.writerow(string.ascii_lowercase[:lehe])
    for line in sys.stdin:
        w.writerow(build(speced, line))

def run_tests():
    import doctest
    doctest.testmod()

def main(args):
    if len(args) < 2:
      print('nothing to do')
      return
    arg = args[1]
    if arg == 'test':
        run_tests()
    else:
       run(arg)


if __name__ == "__main__":
    main(sys.argv)
