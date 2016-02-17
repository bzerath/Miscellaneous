# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # Everything is UTF-8

import os
import random
from pprint import pprint
import LibDice
import time

ECHANTILLON = int(1e9)
# NOMBRE_A_CHERCHER = 2
# NOMBRE_TROUVE = 0
VERBOSE = False
STATS = [0]*100
ALTERNATIF = False  # False: 4.686341, True: 4.648358
partie_la_plus_grande = []


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


def rand(dice):
    if ALTERNATIF:
        for i in xrange(random.randint(0, 9)):
            myseed = random.random()
            random.seed(myseed)
    return random.randint(1, dice)


def game_lite():
    global partie_la_plus_grande
    j = 0
    debut = time.time()
    fichier = open("dice.txt", "w")
    fichier.close()

    while len(partie_la_plus_grande) <= 99:
        j += 1
        if j % 1000000 == 0:
            now = time.time()
            print j, "("+str(now-debut)+"sec)"
            # print float(j)*100/ECHANTILLON, "%", "("+str(now-debut)+"sec)"  # , moy=", float(total)/(j+1)
            debut = now
        dice = 100
        game = True
        partie_la_plus_grande_temp = []
        while game:
            dice_new = random.randint(1, dice)
            partie_la_plus_grande_temp.append(dice_new)
            if len(partie_la_plus_grande_temp) >= len(partie_la_plus_grande):
                partie_la_plus_grande = partie_la_plus_grande_temp[:]
                print j, ":", len(partie_la_plus_grande), "==>", " -> ".join([str(p) for p in partie_la_plus_grande])
                with open("dice.txt", "a") as f:
                    f.write(str(j) + " : " + str(len(partie_la_plus_grande)) + " ==> " + " -> ".join([str(p) for p in partie_la_plus_grande]) + "\n")
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


def game(joueurs):
    # global NOMBRE_A_CHERCHER
    # global NOMBRE_TROUVE
    global VERBOSE
    global STATS
    global partie_la_plus_grande
    ordre_des_joueurs = joueurs.keys()
    # print "Order =", ordre_des_joueurs

    total = 0
    j = 0
    debut = time.time()
    fichier = open("dice.txt", "w")
    fichier.close()

    # for j in xrange(ECHANTILLON):
    while len(partie_la_plus_grande) <= 100:
        j += 1
        if j % 1000000 == 0:
            now = time.time()
            print j, "("+str(now-debut)+"sec)"
            # print float(j)*100/ECHANTILLON, "%", "("+str(now-debut)+"sec)"  # , moy=", float(total)/(j+1)
            debut = now
        nbtours = 0.
        dice = 100
        game = True
        if VERBOSE:
            print "Order =", ordre_des_joueurs
        partie_la_plus_grande_temp = []
        while game:
            # For each player
            for i in xrange(len(ordre_des_joueurs)):
                nbtours += 1
                joueur = ordre_des_joueurs[i]

                dice_new = rand(dice)
                partie_la_plus_grande_temp.append((joueur, dice_new))
                if len(partie_la_plus_grande_temp) >= len(partie_la_plus_grande):
                    partie_la_plus_grande = partie_la_plus_grande_temp[:]
                    print j, ":", len(partie_la_plus_grande), "==>", " -> ".join([str(p[1]) for p in partie_la_plus_grande])
                    with open("dice.txt", "a") as f:
                        f.write(str(j) + " : " + str(len(partie_la_plus_grande)) + " ==> " + " -> ".join([str(p[1]) for p in partie_la_plus_grande]) + "\n")
                if dice_new == 100 or dice_new != dice:
                    STATS[dice_new-1] += 1

                if VERBOSE:
                    print "{nom} rolls the dice : 1d{dice} = {result} !".format(nom=joueur,
                                                                                dice=dice,
                                                                                result=dice_new)
                if dice_new == 1 and dice == 100:
                    if VERBOSE:
                        print "Everybody wins 100/(players-1) points except {name} !".format(name=joueur)
                    for joueur_win in joueurs:
                        if joueur_win != joueur:
                            joueurs[joueur_win] += int(100 / (len(joueurs)-1))
                    game = False
                    ordre_des_joueurs = ordre_des_joueurs[i-1:]+ordre_des_joueurs[:i-1]
                    break
                elif dice_new == dice:
                    # NOMBRE_TROUVE += 1
                    if VERBOSE:
                        print "{name} wins the game !".format(name=joueur)
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
        #total += nbtours
        if VERBOSE:
            print  # total, "\n"

    return total


if __name__ == "__main__":
    LibDice.game_lite()


    # prenoms = []
    # print "C'est parti pour", ECHANTILLON, "parties."
    #
    # with open(os.path.join("Inputs", "Names.txt"), "r") as fichier:
    #     for ligne in fichier.readlines():
    #         prenoms.append(ligne.replace("\n", ""))
    # random.shuffle(prenoms)
    #
    # joueurs = {}
    # for i in xrange(5):
    #     joueurs[prenoms[i]] = 0
    #
    # NbTours = game(joueurs)
    #
    # pprint(joueurs)
    # print 'Bilan sur {nb} parties :'.format(nb=ECHANTILLON)
    # print "moyenne =", NbTours/ECHANTILLON
    # # print "Chances d'avoir /dice X = X :", float(NOMBRE_TROUVE)*100/ECHANTILLON
    # print "Détails :", [float(a)*100/ECHANTILLON for a in STATS]
    # print "Partie la plus longue : ", len(partie_la_plus_grande), "==>", " -> ".join([str(p[1]) for p in partie_la_plus_grande])
    #
    # """test_random = 0.
    # for i in xrange(ECHANTILLON):
    #     test_random += random.random()
    # print test_random/ECHANTILLON"""






