# -*- coding: utf-8 -*-

u"""
Чтобы обращаться к элементам словаря как к полям объекта.
"""

class DictObject:
    def __init__(self, d): 
        self.__dict__.update(d)



