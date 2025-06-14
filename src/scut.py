#!/usr/bin/env python3

import sys

import lib
import output

def process(spec):
    """
    >>> lib.Flow() | process('1-12') | list < "lrwxr-xr-- 1 user group    123 May 25 16:24 'cpu info' -> /proc/cpuinfo"
    ['lrwxr-xr--', '1', 'user', 'group', '123', 'May', '25', '16:24', "'cpu", "info'", '->', '/proc/cpuinfo']
    >>> lib.Flow() | process('1-5,6+7+8,9-12') | list < "lrwxr-xr-- 1 user group    123 May 25 16:24 'cpu info' -> /proc/cpuinfo"
    ['lrwxr-xr--', '1', 'user', 'group', '123', 'May 25 16:24', "'cpu", "info'", '->', '/proc/cpuinfo']
    """
    def _process(line):
        def glue(select):
            if '-' in select:
                [arg1, arg2] = select.split('-')
                start = len(arg1) == 0 and None or int(arg1)
                end = len(arg2) == 0 and None or int(arg2)
                return lib.pick_range(start, end)
            if '+' in select:
                args = select.split('+')
                indices = (int(i) for i in args)
                return lib.concat(indices, ' ')
            index = int(select)
            return lib.pick(index)
        glues = (glue(select) for select in spec.split(','))
        return lib.blend(lib.split(' \t\n\r'), *glues)([line])
    return _process

def run(spec):
    rows = (list(process(spec)(line)) for line in sys.stdin)
    output.output_csv_gen_head(rows, sys.stdout)

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