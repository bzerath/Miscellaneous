# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # Everything is UTF-8

import os
import random
from pprint import pprint

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

if __name__ == "__main__":
    prenoms = []
    joueurs = {}
    with open(os.path.join("Inputs", "Names.txt"), "r") as fichier:
        for ligne in fichier.readlines():
            prenoms.append(ligne.replace("\n", ""))
    random.shuffle(prenoms)

    nombre_de_joueurs = get_number_players()
    for i in xrange(nombre_de_joueurs):
        joueurs[prenoms[i]] = 0

    ordre_des_joueurs = joueurs.keys()
    print "Order =", ordre_des_joueurs

    on_joue = get_begin()
    while (on_joue):
        dice = 100
        game = True
        print "Order =", ordre_des_joueurs
        while game:
            for i in xrange(len(ordre_des_joueurs)):
                joueur = ordre_des_joueurs[i]

                dice_new = random.randint(1, dice)
                print "{nom} rolls the dice : 1d{dice} = {result} !".format(nom=joueur,
                                                                            dice=dice,
                                                                            result=dice_new)
                if dice_new == 1 and dice == 100:
                    print "Everybody wins 100/(players-1) points except {name} !".format(name=joueur)
                    for joueur_win in joueurs:
                        if joueur_win != joueur:
                            joueurs[joueur_win] += int(100 / (len(joueurs)-1))
                    game = False
                    ordre_des_joueurs = ordre_des_joueurs[i-1:]+ordre_des_joueurs[:i-1]
                    break
                elif dice_new == dice:
                    print "{name} wins the game !".format(name=joueur)
                    joueurs[joueur] += dice_new
                    game = False
                    ordre_des_joueurs = ordre_des_joueurs[i:]+ordre_des_joueurs[:i]
                    break
                elif dice_new == 1 and dice != 100:
                    print "{name} makes {name2} win the game !".format(name=joueur,
                                                                       name2=ordre_des_joueurs[i-1])
                    joueurs[ordre_des_joueurs[i-1]] += 2*dice
                    game = False
                    ordre_des_joueurs = ordre_des_joueurs[i-1:]+ordre_des_joueurs[:i-1]
                    break
                else:
                    dice = dice_new

        pprint(joueurs)
        on_joue = get_begin()






