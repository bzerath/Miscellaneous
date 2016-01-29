# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # Everything is UTF-8

import os
import random
from pprint import pprint

ECHANTILLON = int(1e6)
NOMBRE_A_CHERCHER = 2
NOMBRE_TROUVE = 0
VERBOSE = False
STATS = [0]*100


def get_begin():
    begin = raw_input("Begin? (Y/N) ")
    while begin != "Y" and begin != "N":
        begin = raw_input("Begin? (Y/N)")
    return True if begin == "Y" else False


def get_number_players():
    nombre_de_joueurs = raw_input("How many players? ")
    try:
        return int(nombre_de_joueurs)
    except ValueError :
        print "Please give a number."
        return get_number_players()


def game(joueurs):
    global NOMBRE_A_CHERCHER
    global NOMBRE_TROUVE
    global VERBOSE
    global STATS
    ordre_des_joueurs = joueurs.keys()
    #print "Order =", ordre_des_joueurs

    total = 0

    for j in xrange(ECHANTILLON):
        if j % 100000 == 0:
            print float(j)*100/ECHANTILLON, float(total)/(j+1)
        nbtours = 0.
        dice = 100
        game = True
        if VERBOSE: print "Order =", ordre_des_joueurs
        while game:
            for i in xrange(len(ordre_des_joueurs)):
                nbtours += 1
                joueur = ordre_des_joueurs[i]

                dice_new = random.randint(1, dice)
                if dice_new == 100 or dice_new != dice:
                    STATS[dice_new-1] += 1

                if VERBOSE:
                    print "{nom} rolls the dice : 1d{dice} = {result} !".format(nom=joueur,
                                                                                dice=dice,
                                                                                result=dice_new)
                if dice_new == 1 and dice == 100:
                    if VERBOSE: print "Everybody wins 100/(players-1) points except {name} !".format(name=joueur)
                    for joueur_win in joueurs:
                        if joueur_win != joueur:
                            joueurs[joueur_win] += int(100 / (len(joueurs)-1))
                    game = False
                    ordre_des_joueurs = ordre_des_joueurs[i-1:]+ordre_des_joueurs[:i-1]
                    break
                elif dice_new == dice:
                    NOMBRE_TROUVE += 1
                    if VERBOSE: print "{name} wins the game !".format(name=joueur)
                    joueurs[joueur] += dice_new
                    game = False
                    ordre_des_joueurs = ordre_des_joueurs[i:]+ordre_des_joueurs[:i]
                    break
                elif dice_new == 1 and dice != 100:
                    if VERBOSE:
                        print "{name} makes {name2} win the game !".format(name=joueur,
                                                                           name2=ordre_des_joueurs[i-1])
                    joueurs[ordre_des_joueurs[i-1]] += 2*dice
                    game = False
                    ordre_des_joueurs = ordre_des_joueurs[i-1:]+ordre_des_joueurs[:i-1]
                    break
                else:
                    dice = dice_new
        total += nbtours
        if VERBOSE: print total, "\n"

    return total


if __name__ == "__main__":
    prenoms = []

    with open(os.path.join("Inputs", "Names.txt"), "r") as fichier:
        for ligne in fichier.readlines():
            prenoms.append(ligne.replace("\n", ""))
    random.shuffle(prenoms)

    joueurs = {}
    for i in xrange(5):
        joueurs[prenoms[i]] = 0

    NbTours = game(joueurs)

    pprint(joueurs)
    print 'Bilan sur {nb} parties :'.format(nb=ECHANTILLON)
    print "moyenne =", NbTours/ECHANTILLON
    print "Chances d'avoir /dice X = X :", float(NOMBRE_TROUVE)*100/ECHANTILLON
    print "Détails :", [float(a)*100/ECHANTILLON for a in STATS]







