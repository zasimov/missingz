# -*- coding: utf-8 -*-

__author__ = "Zasimov Alexey"
__email__ = "zasimov-a@yandex-team.ru"

u"""
Полезный модуль, загружающий данные из csv-файла с двухколоночной таблицей в
словарь.
"""


import csv


def csvdict(filename, keyfunc=lambda x: x, valuefunc=lambda x: x, delimiter=";"):
    u""" Загружает данные из csv-файла в словарь. Дубликаты
    пропускаются. В словаре останется значение, которое ниже всех.
    """
    with open(filename, "rb") as csvfile:
        d = {}
        n = 1
        rows = csv.reader(csvfile, delimiter=delimiter)
        for row in rows:
            if len(row) != 2:
                raise ValueError("in %s:%s: expected row with 2 values, but received %s values" % (filename, n, len(row)))
            d[keyfunc(row[0])] = valuefunc(row[1])
            n = n + 1
        return d

def csvdictnodups(filename, keyfunc=lambda x: x, valuefunc=lambda x: x, delimiter=";"):
    with open(filename, "rb") as csvfile:
        d = {}
        n = 1
        rows = csv.reader(csvfile, delimiter=delimiter)
        for row in rows:
            if len(row) != 2:
                raise ValueError("in %s:%s: expected row with 2 values, but received %s values" % (filename, n, len(row)))
            key = keyfunc(row[0])
            if key in d:
                raise ValueError("in %s:%s: duplicate key %s" % (filename, n, key))
            d[key] = valuefunc(row[1])
            n = n + 1
        return d
