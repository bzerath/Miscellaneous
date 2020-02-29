# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # Everything is UTF-8

import os
from pprint import pprint
import datetime
from collections import defaultdict
import time
import random

VERBOSE = False


def get_begin():
    begin = input("Begin? (Y/N) ")
    while begin != "Y" and begin != "N":
        begin = input("Begin? (Y/N)")
    return True if begin == "Y" else False


def get_number_players():
    nombre_de_joueurs = input("How many players? ")
    try:
        return int(nombre_de_joueurs)
    except ValueError :
        print("Please give a number.")
        return get_number_players()


def print_int(number):
    number = str(int(number))
    output = []
    mille = 0
    for digit in reversed(number):
        mille += 1
        output = [digit] + output
        if mille == 3:
            output = ["'"] + output
            mille = 0
    if output[0] == "'":
        del(output[0])
    return "".join(output)


def rand(dice):
    return random.randint(1, dice)


def game_lite():
    global partie_la_plus_grande
    j = 0
    debut = time.time()

    while j < 5000000:
        j += 1
        if j % 1000 == 0:
            now = time.time()
            print(j, "("+str(now-debut)+"sec)")
            debut = now
        dice = 100
        game = True
        partie_la_plus_grande_temp = []
        while game:
            dice_new = random.randint(1, dice)
            partie_la_plus_grande_temp.append(dice_new)
            if len(partie_la_plus_grande_temp) >= len(partie_la_plus_grande):
                partie_la_plus_grande = partie_la_plus_grande_temp[:]
                print(j, ":", len(partie_la_plus_grande), "==>", " -> ".join([str(p) for p in partie_la_plus_grande]))
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


def update_file(file_path, parties, echantillon):
    width = max(parties.keys())
    lines_to_render = [str(echantillon)] + \
                      [str(float(parties.get(i, 0))*100/echantillon)
                       for i in range(1, int(width)+1)]
    # print lines_to_render
    with open(file_path, "a") as fichier:
        fichier.write("\t".join(lines_to_render) + "\n")


def game(joueurs, filepath):
    partie_la_plus_grande = []
    ordre_des_joueurs = list(joueurs.keys())
    nombre_de_parties = defaultdict(int)
    print("Order =", ordre_des_joueurs)

    total_de_nb_tours = 0.
    j = 0
    debut = int(time.time())

    try:
        while len(partie_la_plus_grande) <= 99:
            j += 1
            if j % 100000000 == 0:
                now = int(time.time())
                print(j,
                      datetime.datetime.now().strftime("%d-%m_%H:%M"),
                      datetime.timedelta(seconds=now-debut),
                      total_de_nb_tours/j,
                      print_int(j/(now-debut)))
                update_file(filepath, nombre_de_parties, j)
                # debut = now
            nbtours = 0
            dice = 100
            game = True
            if VERBOSE:
                print("Order =", ordre_des_joueurs)
            partie_actuelle = []
            while game:
                # For each player
                for i in range(len(ordre_des_joueurs)):
                    nbtours += 1
                    joueur = ordre_des_joueurs[i]

                    dice_new = rand(dice)
                    partie_actuelle.append((joueur, dice_new))
                    if len(partie_actuelle) >= len(partie_la_plus_grande):
                        partie_la_plus_grande = partie_actuelle[:]
                        print(" ".join([
                            print_int(j), ":",
                            str(len(partie_la_plus_grande)), "==>",
                            "->".join([str(p[1]) for p in partie_la_plus_grande])]))
                    if VERBOSE:
                        print("{nom} rolls the dice : 1d{dice} = {result} !".format(nom=joueur,
                                                                                    dice=dice,
                                                                                    result=dice_new))
                    if dice_new == 1 and dice == 100:
                        if VERBOSE:
                            print("Player {name} looses 100 points !".format(name=joueur))
                        joueurs[joueur] -= 100
                        game = False
                        ordre_des_joueurs = ordre_des_joueurs[i-1:]+ordre_des_joueurs[:i-1]
                        break
                    elif dice_new == dice:
                        if VERBOSE:
                            print("{name} wins the game !".format(name=joueur))
                        joueurs[joueur] += dice_new
                        game = False
                        ordre_des_joueurs = ordre_des_joueurs[i:]+ordre_des_joueurs[:i]
                        break
                    elif dice_new == 1 and dice != 100:
                        if VERBOSE:
                            print("{name} makes {name2} win the game !".format(name=joueur,
                                                                               name2=ordre_des_joueurs[i-1]))
                        joueurs[ordre_des_joueurs[i-1]] += 2*dice
                        game = False
                        ordre_des_joueurs = ordre_des_joueurs[i-1:]+ordre_des_joueurs[:i-1]
                        break
                    else:
                        dice = dice_new
            if len(partie_actuelle) >= len(partie_la_plus_grande) \
                    and nombre_de_parties:
                update_file(filepath, nombre_de_parties, j)
            total_de_nb_tours += nbtours
            nombre_de_parties[nbtours] += 1
            if VERBOSE:
                print(total_de_nb_tours, "\n")
    except:
        print("Fin forcee...")

    return total_de_nb_tours, partie_la_plus_grande, j, nombre_de_parties


if __name__ == "__main__":
    # LibDice.game_lite()
    #
    # print "\n-----------------\n"
    #
    # game_lite()

    prenoms = []
    filepath = "output_dice.tsv"

    with open(os.path.join("Inputs", "Names.txt"), "r") as fichier:
        for ligne in fichier.readlines():
            prenoms.append(ligne.replace("\n", ""))
    random.shuffle(prenoms)

    joueurs = {}
    for i in range(20):
        joueurs[prenoms[i]] = 0

    begin = time.time()
    NbTours, partie_la_plus_grande, echantillon, nombre_de_parties = game(joueurs, filepath)
    end = time.time()

    print("--------")
    print("Scores :")
    pprint(joueurs)
    print("--------")
    print("Durée pour {nb_total} parties : {temps} secondes ({nb_ratio}/sec)".format(
        nb_total=print_int(echantillon),
        temps=int(end-begin),
        nb_ratio=print_int(echantillon/(end-begin))))
    print('Bilan sur {nb} parties :'.format(nb=print_int(echantillon)))
    print("\tMoyenne de nombre de tours =", NbTours / echantillon)
    print("\tPartie la plus longue : \n\t\t",
          len(partie_la_plus_grande),
          "==>",
          " -> ".join([str(p[1]) for p in partie_la_plus_grande]))
    probabilites = [(key, float(value) * 100 / echantillon) for key, value in nombre_de_parties.items()]
    probabilites.sort(key=lambda colonnes: colonnes[1], reverse=True)
    print(sum(p[1] for p in probabilites))
    for nbt, proba in probabilites:
        print("{} tours : {}%".format(int(nbt), proba))

    update_file(filepath, nombre_de_parties, echantillon)
