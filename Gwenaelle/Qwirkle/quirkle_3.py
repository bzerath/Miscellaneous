import termcolor
import pprint
import random


FORMES = {
    "croix": "X",
    "losange": "♦",
    "cercle": "●",
    "carré": "■",
    "étoile": "☼",
    "trèfle": "♣"
}
COULEURS = {
    "rouge": "red",
    "violet": "magenta",
    "bleu": "blue",
    "gris": "white",  # pas d'orange en console
    "vert": "green",
    "jaune": "yellow",
}
NOMBRE_DE_JOUEURS = 3
NOMBRE_DE_CARTE_PAR_MAIN = 6

NOMBRE_DE_TUILES_IDENTIQUES = 3

COULEUR = "couleur"
FORME = "forme"


def render_hand(hand, sep="\t"):
    output = []
    for carte in hand:
        try:
            forme = FORMES[carte[0]]
            couleur = COULEURS[carte[1]]
            output.append(termcolor.colored(forme, couleur))
        except TypeError:
            output.append(termcolor.colored(" ", None))
    return sep.join(output)


def extract_bigger_categories(categories):
    maximum = categories[0]
    for i in range(len(categories)):
        if categories[i][1] > maximum[1]:
            maximum = categories[i]
    return maximum


def get_bigger_set_of_cards(hand):
    color_sets = {color: set() for color in COULEURS}
    formes_sets = {forme: set() for forme in FORMES}

    for forme, couleur in hand:
        color_sets[couleur].add((forme, couleur))
        formes_sets[forme].add((forme, couleur))

    # à partir du dictionnaire color_sets -> une liste de tuples [(couleur, nombre de cartes de cette couleur), ...]
    colors_count = []
    for color in color_sets:
        tuple_temp = (color, len(color_sets[color]))
        colors_count.append(tuple_temp)
    formes_count = []
    for forme in formes_sets:
        tuple_temp = (forme, len(formes_sets[forme]))
        formes_count.append(tuple_temp)
    most_found_color = extract_bigger_categories(colors_count)
    most_found_forme = extract_bigger_categories(formes_count)

    if most_found_color[1] >= most_found_forme[1]:
        return COULEUR, most_found_color
    else:
        return FORME, most_found_forme


def get_first_player(joueurs: dict):
    # for joueur in joueurs:
    #     print(joueur, "\t", render_hand(joueurs[joueur]))
    #     print(get_bigger_set_of_cards(joueurs[joueur]))
    joueurs_sets = {}
    for joueur in joueurs:
        joueurs_sets[joueur] = get_bigger_set_of_cards(joueurs[joueur])
    print(joueurs_sets)

    maximum = (list(joueurs_sets.keys())[0], joueurs_sets[list(joueurs_sets.keys())[0]])
    for joueur in joueurs_sets:
        number = joueurs_sets[joueur][1][1]
        if number > maximum[1][1][1]:
            maximum = (joueur, joueurs_sets[joueur])

    return maximum


def main():
    # Une tuile = un tuple <(forme, couleur)>
    # Préparer le jeu (108 cartes = 6 formes * 6 couleurs * 3)
    paquet = []
    for i in range(NOMBRE_DE_TUILES_IDENTIQUES):
        for forme in FORMES:
            for couleur in COULEURS:
                tuile = (forme, couleur)
                paquet.append(tuile)
    random.shuffle(paquet)
    random.shuffle(paquet)
    random.shuffle(paquet)

    # Piocher 6 cartes par personne
    joueurs = {}
    for i in range(NOMBRE_DE_JOUEURS):
        joueurs[i] = []
        for j in range(NOMBRE_DE_CARTE_PAR_MAIN):
            joueurs[i].append(paquet.pop(0))

    for joueur in joueurs:
        print(joueur, "\t", render_hand(joueurs[joueur]))

    first_player = get_first_player(joueurs)
    print("The player n°{player_num} will play first, because he has the biggest set ({category}), "
          "with {number} {type_}.".format(player_num=first_player[0],
                                          category=first_player[1][0],
                                          number=first_player[1][1][1],
                                          type_=first_player[1][1][0]))

    # Poser les cartes du premier joueur sur le plateau, à la verticale, en partant de (0, 0)

    # Le premier joueur pioche les cartes qui lui manquent
    # -> On compte les points

    # Là on commence la boucle
    # Faire un while jusqu'à ce que la pioche soit vide, qui itère sur la liste des joueurs, en partant du joueur *suivant*
    # -> joueur choisit ses tuiles
    # -> vérifier que la sélection est correcte selon les règles du jeu
    # -> Si OK, passer au choix des coordonnées, sinon rester sur le choix des tuiles
    # -> joueur choisit les positions
    # -> vérifier que les positions sont correctes selon les règles du jeu
    #    --> autant de coordonnées que de cartes choisies
    #    --> coordonnées sont libres
    #    --> pas de doublon (ligne ou colonne ?)
    #    --> colonne ou ligne ininterrompue
    # -> si OK, ajouter les choix au dico board
    # -> On compte les points
    # -> joueur pioche
    # -> render_board
    # Passer au jouer *suivant*

    # etc...


def render_board(board: dict):
    # Analyser les coordonnées pour avoir la dimension de la future matrice
    list_of_numline = []
    list_of_numcol = []
    for key in board:
        list_of_numline.append(key[0])
        list_of_numcol.append(key[1])

    # Avoir les bornes de chaque dimension pour faire un range(min, max)
    # TODO: faire ça avec la méthode de recherche min/max vue en cours
    min_line = min(list_of_numline)
    max_line = max(list_of_numline)
    min_col = min(list_of_numcol)
    max_col = max(list_of_numcol)

    valeur_case_vide = None

    matrix_output = []
    for numline in range(min_line, max_line+1):
        line_temp = []
        for numcol in range(min_col, max_col+1):
            line_temp.append(board.get((numline, numcol),
                                       valeur_case_vide))
        matrix_output.append(line_temp)

    line_of_numcols = ""
    for i in range(min_col, max_col+1):
        line_of_numcols += str(i) + "\t"
    print("\t", termcolor.colored(line_of_numcols, "grey"))
    list_of_numlines = list(range(min_line, max_line+1))
    for i, ligne in enumerate(matrix_output):
        print(termcolor.colored(list_of_numlines[i], "grey"),
              "\t", render_hand(ligne))



if __name__ == "__main__":
    main()
    #               (y, x):     ( forme,     couleur)
    dico_example = {(0, 0):     ('losange', 'violet'),
                    (1, 0):     ('croix',   'violet'),
                    (2, 0):     ('cercle',  'violet'),
                    (-1, 0):    ('étoile',  'violet'),
                    (2, -1):    ('cercle',  'gris'),
                    (0, 1):     ('losange', 'vert'),
                    (-1, 1):    ('étoile',  'vert')}
    dico_example_2 = {(0, 0): ('losange', 'violet'),
                      (1, 0): ('croix', 'violet'),
                      (2, 0): ('cercle', 'violet'),
                      (-1, 0): ('étoile', 'violet'),
                      (2, -1): ('cercle', 'gris'),
                      (0, 1): ('losange', 'vert'),
                      (-1, 1): ('étoile', 'vert'),
                      (0, -1): ('losange', 'bleu'),
                      (0, 2): ('losange', 'jaune'),
                      (-1, 2): ('étoile', 'jaune')}
    dico_example_3 = {(0, 0): ('losange', 'violet'),
                      (1, 0): ('croix', 'violet'),
                      (2, 0): ('cercle', 'violet'),
                      (-1, 0): ('étoile', 'violet'),
                      (2, -1): ('cercle', 'gris'),
                      (0, 1): ('losange', 'vert'),
                      (-1, 1): ('étoile', 'vert'),
                      (0, -1): ('losange', 'bleu'),
                      (0, 2): ('losange', 'jaune'),
                      (-1, 2): ('étoile', 'jaune'),
                      (-2, -2): ('croix', 'bleu')}


    # render_board(dico_example)
    render_board(dico_example_2)
