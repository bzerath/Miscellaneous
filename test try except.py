# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # Everything is UTF-8


def f1(i):
    try:
        return 1/i
    except ZeroDivisionError:
        print "ZeroDivisionError"
        raise


def f2(i):
    try:
        return f1(i)
    except Exception as e:
        print "impossible"


if __name__ == "__main__":
    pass
    print f2(1)
    print f2(0)
