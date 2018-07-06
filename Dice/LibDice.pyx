# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # Everything is UTF-8
import time
import random
import numpy

# $ python setup.py build_ext --inplace

def game_lite():
    game_lite_c()


cdef void game_lite_c():
    cdef long j = 0
    cdef double now
    cdef double debut
    cdef int dice
    cdef int dice_new
    cdef bint game

    partie_la_plus_grande = []
    debut = time.time()

    while j < 5000000:
        j += 1
        if j % 1000000 == 0:
            now = time.time()
            print j, "("+str(now-debut)+"sec)"
            debut = now
        dice = 100
        game = True
        partie_la_plus_grande_temp = []
        while game:
            dice_new = numpy.random.randint(1, dice)
            partie_la_plus_grande_temp.append(dice_new)
            if len(partie_la_plus_grande_temp) >= len(partie_la_plus_grande):
                partie_la_plus_grande = partie_la_plus_grande_temp[:]
                print j, ":", len(partie_la_plus_grande), "==>", " -> ".join([str(p) for p in partie_la_plus_grande])
            if dice_new == 1 and dice == 100:
                game = False
                break
            elif dice_new == dice:
                game = False
                break
            elif dice_new == 1 and dice != 100:
                game = False
                break
            else:
                dice = dice_new


if __name__ == "__main__":
    pass

