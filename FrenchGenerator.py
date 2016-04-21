# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # Everything is UTF-8
import sys
sys.setdefaultencoding('utf-8')
import random

"""
C'est de la merde.
"""

values = {"a": 7.88175306,
          "b": 0.929997316,
          "c": 3.364918148,
          "d": 3.787081192,
          "e": 15.18857992,
          "f": 1.100307591,
          "g": 0.893870894,
          "h": 0.760719225,
          "i": 7.771309428,
          "j": 0.562539997,
          "k": 0.050576991,
          "l": 5.631593072,
          "m": 3.063520571,
          "n": 7.323341797,
          "o": 5.55108276,
          "p": 3.118226296,
          "q": 1.405833901,
          "r": 6.763898351,
          "s": 8.203794306,
          "t": 7.477137136,
          "u": 6.514109948,
          "v": 1.680394707,
          "w": 0.117668917,
          "x": 0.399455007,
          "y": 0.317912512,
          "z": 0.140376953
          }

def generate(length):
    word = []
    while not rules(word):
        # We take a letter in the alphabet
        letter = random.choice(values.keys())
        # We try to add it
        if random.random()*100 < values[letter]:
            word.append(letter)
    return word


def rules(mot):
    if "s" in mot and "c" in mot and "t" in mot and compterVoyelles(mot) >= 2 and compterS(mot) >= 2:
        return True

def compterVoyelles(mot):
    voyelles = "aeiouy"
    nb = 0
    for lettre in mot:
        if lettre in voyelles:
            nb += 1
    return nb

def compterS(mot):
    return len([lettre for lettre in mot if lettre == "s"])

if __name__ == "__main__":
    length = 10
    mot_trouves = 0

    while mot_trouves < 30:
        mot = generate(length)
        if len(mot) < length:
            print "".join(mot)
            mot_trouves += 1

