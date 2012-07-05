# -*- coding: utf-8 -*-

__author__ = "Zasimov Alexey"
__email__ = "zasimov-a@yandex-team.ru"

u"""
Предположим, что есть список ['a', 'b', 'c']. Нам нужно быстро отображать
элемент списка на его индекс. В этом списке.
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

