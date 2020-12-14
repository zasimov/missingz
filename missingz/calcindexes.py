__author__ = "Alexey Zasimov"
__email__ = "zasimov@gmail.com"

u"""
Module contains function to construct indexes map.
"""

def indexes(l):
    u"""
    >>> l = ['a', 'b', 'c', 'a']
    >>> i = indexes(l)
    >>> i['a'] == 3
    True
    >>> i['b'] == 1
    True
    """
    d = {}
    for n, item in enumerate(l):
        d[item] = n
    return d

