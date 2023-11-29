def sq(x):
    return x ** 2


def list_like(var):
    return hasattr(var, "__getitem__") and hasattr(var, "__len__")


def is_iter(var):
    return hasattr(var, "__iter__")


# helper for all the checks if optional variables are
# set or not.
def some(v): 
    return not isinstance(v, type(None))


# takes an iterable object and yields pairs of values 
# in a sliding window
def pairs(arr):
    if not is_iter(arr): return None

    iter_arr = iter(arr)
    last = next(iter_arr, None)

    while True:
        current = next(iter_arr, None)
        if some(current):
            yield last, current
            last = current
        else:
            break


def slice_pairs(arr):
    if not is_iter(arr): return None
    iter_arr = iter(arr)

    while True:
        first, second = next(iter_arr, None), next(iter_arr, None)
        if some(first) and some(second):
            yield first, second
        else:
            break


# this would be the proper abstract function, where pairs(a) is just group(a, 2)
def group(arr, groupsize):
    pass



def try_float(s):
    try:
        return float(s), True
    except:
        return None, False


def safe_float(s):
    try:
        return float(s)
    except:
        return None


from math import nan, inf
from labtools import perror
from labtools.libs import numpy as np

def is_real(x):
    return (not np.isnan(x)) and (not np.isinf(x))