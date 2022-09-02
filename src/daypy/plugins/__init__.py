# -*- coding: utf-8 -*-
import timeit
from time import perf_counter


def clear_dict(d):
    if d is None:
        return None
    elif isinstance(d, list):
        return list(filter(lambda x: x is not None, map(clear_dict, d)))
    elif not isinstance(d, dict):
        return d
    else:
        r = dict(
            filter(lambda x: x[1] is not None,
                   map(lambda x: (x[0], clear_dict(x[1])),
                       d.items())))
        if not bool(r):
            return None
        return r


a = {
    'role': 'member',
    'token': 'abcedfg',
    'extra': {
        'mid': 'abc',
        'aid': None,
        'ids': [
            1,
            2,
            None,
            5
        ]
    },
    'timestamp': "2022-09-01 22:08:37"
}

from functools import singledispatch

@singledispatch
def clear(ob):
    return ob

@clear.register(list)
def _process_list(d):
    return [clear(v) for v in d if v]

@clear.register(dict)
def _process_dict(d):
    return {k: clear(v) for k, v in d.items() if v}




if __name__ == '__main__':
    t = perf_counter()
    for _ in range(10000):
        clear(a)
    print(f'coast:{perf_counter() - t:.8f}s')

    t = perf_counter()
    for _ in range(10000):
        clear_dict(a)
    print(f'coast:{perf_counter() - t:.8f}s')
