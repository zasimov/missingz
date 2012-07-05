# -*- coding: utf-8 -*-

u"""
Работаем с csv-файлом как с таблицей.

Модуль умеет брать конкретные поля из файла. Умеет фильтровать строчки
по условию, умеет агрегировать значения колонок.
"""

import csv
from itertools import ifilter, imap
from missingz.typesmap import typesmap


u"""

Базовым является некоторый объект, который выдает строки - контейнер
со строками.

Из этого контейнера при помощи шапки мы можем конструировать
словари. Шапка в общем случае - это любое подмножество множества
допустимых колонок.

Класс Table - базовый класс, создающий из любого итератора - таблицу,
то есть тот, кто именует колонки.

Проекция - это создание новой таблицы, с другим подмножеством колонок.

Шапка - это не только имена колонок, но и их типы! Поэтому для
управления шапкой создается класс Header.

CSV-таблица - это частный случай таблицы.


Как пользоваться:

table = csvtable('mytable.csv', row_wrapper=DictObject)
for row in table:
    print row.field


"""

def parse_typed_csv_header(header_row, namefunc=lambda x: x, typefunc=lambda x: typesmap[x], default_type=str):
    u""" Если мы используем собственный формат описания таблицы, в
    котором колонка описывается строкой: name:type, эта функция
    разбирает такую шапку и выдает два объекта - список имен колонок и
    словарь типов колонок.
    """
    fields = []
    types = {}
    for field in header_row:
        try:
            p = field.index(':')
            name = field[:p]
            typename = field[p+1:]
            type_ = typefunc(typename)
        except ValueError:
            name = field
            type_ = default_type
        name = namefunc(name)
        fields.append(name)
        types[name] = type_
    return fields, types


class Header:
    u"""
    Заголовок таблицы.
    """

    def __init__(self, fields, types={}, def_type=lambda x: x):
        if type(fields) == list:
            # Нумеруем колонки последовательно.
            self.fields = {}
            for index, name in enumerate(fields):
                self.fields[name] = index
        else:
            self.fields = fields.copy()
        self.types = types.copy()
        self.def_type = def_type


    def indexes(self, *fields):
        u"""
        Возвращает индексы колонок fields.
        """
        for field in fields:
            yield self.fields[field]


    def cast(self, field, value):
        u"""
        Приведение типов.
        """
        try:
            return self.types[field](value)
        except KeyError:
            return self.def_type(value)


class Table:
    u"""
    Таблица - именует строки контейнера.
    """

    def __init__(self, header, fields, collection, row_wrapper=lambda x: x):
        u""" header - таблица соответствия между именем и положением
        элемента в строке. Это заголовок таблицы.
        """
        self.header = header
        self.fields = fields[:]
        self._indexes = [index for index in self.header.indexes(*fields)]
        self.collection = list(collection)
        self.row_wrapper = row_wrapper

    def project(self, *fields):
        return Table(self.header, fields, self.collection, self.row_wrapper)

    def filter(self, filterfunc):
        def ff(row):
            return filterfunc(self._givename(row))
        return Table(self.header, self.fields, ifilter(ff, self.collection), self.row_wrapper)

    def _givename(self, row):
        u"""
        Именует каждый элемент строчки row.
        """
        d = {}
        for index, field in zip(self._indexes, self.fields):
            d[field] = self.header.cast(field, row[index])
        return self.row_wrapper(d)

    def __iter__(self):
        u"""
        Создаем из каждой строки контейнера collection словарь.
        """
        return imap(self._givename, self.collection)


def csvtable(filename, types={}, default_type=lambda x: x, \
        row_wrapper=lambda x: x, delimiter=';', quotechar='"'):
    u"""
    Загружает таблицу из csv-файла.
    """
    with open(filename, "rb") as csvfile:
        rows = [row for row in csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)]
    head_fields = rows[0]
    return Table(Header(head_fields, types, default_type), head_fields, rows[1:], row_wrapper)

def typed_csvtable(filename, namefunc=lambda x: x, typefunc=lambda x: typesmap[x], default_type=lambda x: x, \
        row_wrapper=lambda x: x, delimiter=';', quotechar='"'):
    with open(filename, "rb") as csvfile:
        rows = [row for row in csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)]

    head_fields, types = parse_typed_csv_header(rows[0], namefunc=namefunc, typefunc=typefunc, \
            default_type=default_type)

    return Table(Header(head_fields, types, default_type), head_fields, rows[1:], row_wrapper)

