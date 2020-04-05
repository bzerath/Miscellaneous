import random

PATH = "noms.txt"


with open(PATH, mode="r", encoding="utf-8") as fichier_noms:
    lignes_du_fichier = fichier_noms.readlines()
    # print(lignes_du_fichier[0], lignes_du_fichier[-1])
    print(random.choice(lignes_du_fichier))  # renvoie une ligne au hasard dans une liste


with open(PATH, mode="r", encoding="utf-8") as fichier_noms:
    ligne = fichier_noms.readline()
    print(ligne.replace("\n", ""))  # premier nom
    while ligne != "":
        nombre_aleatoire = random.random()
        if nombre_aleatoire > 0.9:
            print(ligne)
        ligne_precedente = ligne
        ligne = fichier_noms.readline()
    print(ligne_precedente.replace("\n", ""))

# "\n" ou "\n\r" --> retour à la ligne
# "\t" --> tabulation

with open(PATH, mode="r", encoding="utf-8") as fichier_noms:
    lignes_du_fichier = fichier_noms.readlines()
    lignes_du_fichier.sort()
    print(lignes_du_fichier)
with open('noms_trie.txt', 'w', encoding='utf-8') as fichier_trie:
    for i in range(len(lignes_du_fichier)):
        fichier_trie.write(lignes_du_fichier[i])

import datetime
now = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
print(now)
with open('noms_trie.txt', 'a', encoding='utf-8') as fichier_trie:
    fichier_trie.write(now)


with open('noms_trie.txt', 'r', encoding='utf-8') as fichier_trie:
    ligne = fichier_trie.readline()
    while ligne != "":
        noms = ligne.replace("\n", "").split(" ")
        print(noms[1])
        ligne = fichier_trie.readline()
