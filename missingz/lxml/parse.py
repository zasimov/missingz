# -*- coding: utf-8 -*-

__author__ = "Zasimov Alexey"
__email__ = "zasimov-a@yandex-team.ru"

u"""
Загружает lxml.

Здесь лежат функции для разбора XML.

  lxml_parse_file - разбора файла, хранящегося на диске.
"""


# Загрузка lxml - http://lxml.de/tutorial.html
try:
  from lxml import etree
  #print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    #print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      #print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        #print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          #print("running with ElementTree")
        except ImportError:
          import sys
          sys.stderr.write("Failed to import ElementTree from any known place\n")
          raise


def lxml_parse(fobj, **kwargs):
    u"""
    Разбирает входной XML-файл. Эта функция нужна лишь для того, чтобы импорт и
    настройка парсера XML лежала в одном модуле.
    """
    tree = etree.parse(fobj, **kwargs)
    tree.xinclude()
    return tree


def lxml_parse_string(s, **kwargs):
  return etree.fromstring(s, **kwargs)


def lxml_parse_file(filename, **kwargs):
    f = open(filename, "r")
    try:
        return parse(f, **kwargs)
    finally:
        f.close()

