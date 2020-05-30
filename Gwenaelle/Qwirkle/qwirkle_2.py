import termcolor
import random
import time


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
NUMBER_OF_EACH_COLOR = 3
NUMBER_OF_COLORS = len(COULEURS)
NUMBER_OF_FORMES = len(FORMES)
NUMBER_OF_PLAYERS = 3
NUMBER_OF_CARDS = 6
COULEUR = "COULEUR"
FORME = "FORME"


def render_hand(hand: list, separator: str = "\t") -> str:
    """ Renvoie un string qui représente la main donnée
    :param hand: liste de tuples (forme, couleur)
    :param separator: par défaut \t
    :return: str
    """
    return separator.join([termcolor.colored(FORMES.get(forme, forme),
                                             COULEURS.get(color, color))
                           for forme, color in hand])


def render_board(board: dict):
    """ Affiche le terrain de jeu avec des tabulations entre chaque colonne

    :param board: dictionnaire représentant le tableau de jeu
    """
    print(board)
    num_lines = [i[0] for i in board.keys()]
    num_columns = [i[1] for i in board.keys()]
    min_num_line, max_num_line = min(num_lines), max(num_lines)
    min_num_col, max_num_col = min(num_columns), max(num_columns)

    matrix_output = []

    for numline in range(min_num_line, max_num_line+1):
        line_temp = []
        for numcol in range(min_num_col, max_num_col+1):
            if (numline, numcol) in board:
                line_temp.append(board[(numline, numcol)])
            else:
                line_temp.append((" ", None))
        matrix_output.append(line_temp)

    print(termcolor.colored("\t" + "\t".join([str(i) for i in sorted(set(num_columns))]), "grey"))
    for i, line in enumerate(matrix_output):
        print(termcolor.colored(sorted(set(num_lines))[i], "grey"),
              "\t", render_hand(line))


def get_bigger_set_of_cards(hand: list):
    """ Return bigger set of cards.

    Returns if the bigger set is a set of colors or of formes, and the len of the set.
    If the bigger set is identical, the bigger set is a set of formes.

    :param hand: list of tuples
    :return:
    """
    color_sets = {color: set() for color in COULEURS}
    formes_set = {forme: set() for forme in FORMES}
    for forme, color in hand:
        color_sets[color].add((forme, color))
        formes_set[forme].add((forme, color))

    color_sets = [(key, len(value)) for key, value in color_sets.items()]
    color_sets.sort(key=lambda x: x[1], reverse=True)
    formes_set = [(key, len(value)) for key, value in formes_set.items()]
    formes_set.sort(key=lambda x: x[1], reverse=True)

    if color_sets[0][1] > formes_set[0][1]:
        return COULEUR, color_sets[0][0], color_sets[0][1]
    else:
        return FORME, formes_set[0][0], formes_set[0][1]


def get_player_with_the_bigger_set(players_games: dict) -> tuple:
    """ Renvoie les informations sur le joueur ayant la plus grande combinaison.
    En cas d'égalité, le plus petit ID de joueur gagne.

    ex: (1, 'COULEUR', 'rouge', 3)

    :param players_games:
    :return: (n° joueur, catégorie de combinaison, valeur, longueur)
    """
    players_sets = []
    for player, hand in players_games.items():
        players_sets.append((player, *get_bigger_set_of_cards(hand)))
    players_sets.sort(key=lambda x: x[3], reverse=True)
    return players_sets[0]


def piocher(hand: list, pioche: list):
    """ Pioche les cartes manquantes pour arriver à 6 cartes par main.

    :param hand: liste de tuples (forme, couleur)
    :param pioche: liste des cartes restantes
    :return:
    """
    cards_to_piocher = 6 - len(hand)
    try:
        for i in range(cards_to_piocher):
            hand.append(pioche.pop(0))
    except IndexError:
        print("Attention : La pioche est vide !")
    return hand, pioche


def sortir_cartes(hand: list, selection: list) -> (list, list):
    """ Extrait les cartes demandées et renvoie la nouvelle main + les cartes sorties.

    :param hand: liste de tuples (forme, couleur)
    :param selection: liste des index de cartes choisies
    :return: new_hand, sorties
    """
    sorties = []
    for i in selection:
        sorties.append(hand[i])
    new_hand = [i for i in hand if i not in sorties]
    return new_hand, sorties


def sortir_cartes_selon_couleur(hand: list, couleur_choisie: str) -> (list, list):
    """ Sort les cartes de la couleur donnée (sans doublon)

    :param hand: liste de tuples (forme, couleur)
    :param couleur_choisie: couleur choisie
    :return: new_hand, sorties
    """
    selection = []
    cartes_selectionnees = []
    for i, (forme, couleur) in enumerate(hand):
        if couleur == couleur_choisie:
            if (forme, couleur) not in cartes_selectionnees:
                selection.append(i)
                cartes_selectionnees.append((forme, couleur))
    return sortir_cartes(hand, selection)


def sortir_cartes_selon_forme(hand: list, forme_choisie: str) -> (list, list):
    """ Sort les cartes de la forme donnée (sans doublon)

    :param hand: liste de tuples (forme, couleur)
    :param forme_choisie: forme choisie
    :return: new_hand, sorties
    """
    selection = []
    cartes_selectionnees = []
    for i, (forme, couleur) in enumerate(hand):
        if forme == forme_choisie:
            if (forme, couleur) not in cartes_selectionnees:
                selection.append(i)
                cartes_selectionnees.append((forme, couleur))
    return sortir_cartes(hand, selection)


def check_selection_is_ok(hand: list, selection: list) -> bool:
    """ Vérifie que une seule forme ou bien une seule couleur a été choisie pour être jouée

    :param hand: liste de tuples (forme, couleur)
    :param selection: liste des index de cartes choisies
    :return: booléen
    """
    couleurs = set()
    formes = set()
    for numero in selection:
        formes.add(hand[numero][0])
        couleurs.add(hand[numero][1])
    if len(formes) > 1 and len(couleurs) > 1:
        return False
    else:
        return True


def check_coordinates_are_ok(coordinates: list, cartes: list, board: dict) -> bool:
    """ Vérifie que les coordonnées de destination obéissent aux règles.

    - Il doit y avoir autant de coordonnées que de cartes choisies
    - Les coordonnées sélectionnées ne sont pas déjà prises
    - Il n'y a pas de doublon sur la ligne (mais colonne OK)
    - TODO Vérifier qu'on forme bien une ligne ou une colonne ininterrompue en incluant le board

    :param coordinates: liste de tuples de coordonnées
    :param cartes: cartes associées aux coordonnées
    :param board: terrain de jeu
    :return: booléen
    """
    if len(coordinates) != len(cartes):
        print("Il doit y avoir autant de coordonnées que de cartes choisies !")
        return False

    for coord in coordinates:
        if coord in board:
            print("Les coordonnées sélectionnées sont déjà prises ! ({})".format(coord))
            return False

    for i in range(len(coordinates)):
        line = [card for coord, card in board.items() if coord[0] == coordinates[i][0]]
        for carte in cartes:
            if carte in line:
                print("La carte {} est déjà présente sur la ligne {} !".format(
                    termcolor.colored(FORMES.get(carte[0], carte[0]),
                                      COULEURS.get(carte[1])),
                    coordinates[0]))
                return False

    # TODO Vérifier qu'on forme bien une ligne ou une colonne ininterrompue en incluant le board

    return True


def main():
    # Conception du paquet de cartes
    paquet = []
    for nforme in range(NUMBER_OF_FORMES):
        for ncolor in range(NUMBER_OF_COLORS):
            for nrepet in range(NUMBER_OF_EACH_COLOR):
                paquet.append((list(FORMES.keys())[nforme],
                               list(COULEURS.keys())[ncolor]))
    # On mélange le paquet
    random.shuffle(paquet)
    random.shuffle(paquet)
    random.shuffle(paquet)

    # Distribution des cartes
    players_games = {i: [] for i in range(NUMBER_OF_PLAYERS)}
    for card in range(NUMBER_OF_CARDS):
        for num_player in range(NUMBER_OF_PLAYERS):
            players_games[num_player].append(paquet.pop(0))

    # Pour le débug, on affiche les jeux de tout le monde
    for player in players_games:
        print("Joueur n°{}".format(player), "\t", render_hand(players_games[player]))

    # Select first player to play
    first_player, global_type, type_, number = get_player_with_the_bigger_set(players_games)
    print("Player {} plays first, because he has {} cards with the same {} ({}).".format(
        first_player, number, global_type, type_
    ))

    # Put the cards on the board
    if global_type == COULEUR:
        players_games[first_player], cartes = sortir_cartes_selon_couleur(players_games[first_player],
                                                                          type_)
    else:
        players_games[first_player], cartes = sortir_cartes_selon_forme(players_games[first_player],
                                                                        type_)
    board = {}
    for i, carte in enumerate(cartes):
        board[(i, 0)] = carte
    render_board(board)

    # First player pioche
    print("Player {} pioche {} cards, {} cards remain in pioche.".format(first_player,
                                                                         6-len(players_games[first_player]),
                                                                         len(paquet)))
    players_games[first_player], paquet = piocher(players_games[first_player], paquet)

    # Let's play
    game_is_on = True
    num_player = first_player
    while game_is_on:
        # Let the next player play
        time.sleep(1)
        if num_player == max(players_games.keys()):
            num_player = 0
        else:
            num_player += 1

        print("Player {} joue !".format(num_player))
        print("Cartes :", render_hand(players_games[num_player]))
        reponse = input("Quelles cartes voulez-vous jouer ? (de 0 à 5, séparé par des virgules)\n")
        liste = [int(i) for i in reponse.replace(" ", "").split(",")]
        if check_selection_is_ok(players_games[num_player], selection=liste):
            players_games[num_player], cartes_a_jouer = sortir_cartes(hand=players_games[num_player],
                                                                      selection=liste)
            # Sélectionner la destination
            reponse = input("Où voulez-vous placer {} ? "
                            "Rappel : les coordonnées sont (num_ligne, num_colonne). "
                            "ex: '(0, 1); (1, 1)'\n".format(render_hand(cartes_a_jouer,
                                                                        separator="")))
            reponse = reponse.replace(" ", "")
            coordinates = [eval(coord) for coord in reponse.split(";")]
            while not check_coordinates_are_ok(coordinates=coordinates,
                                               board=board,
                                               cartes=cartes_a_jouer):
                reponse = input("Où voulez-vous placer {} ? "
                                "Rappel : les coordonnées sont (num_ligne, num_colonne). "
                                "ex: '(0, 1); (1, 1)'\n".format(render_hand(cartes_a_jouer, separator="")))
                reponse = reponse.replace(" ", "")
                coordinates = [eval(coord) for coord in reponse.split(";")]
            for i in range(len(coordinates)):
                print(coordinates[i], cartes_a_jouer[i])
                board[coordinates[i]] = cartes_a_jouer[i]

            print("Player {} pioche {} cards, {} cards remain in pioche.".format(num_player,
                                                                                 6 - len(players_games[num_player]),
                                                                                 len(paquet)))
            players_games[num_player], paquet = piocher(players_games[num_player], paquet)

            render_board(board)


if __name__ == "__main__":
    main()


