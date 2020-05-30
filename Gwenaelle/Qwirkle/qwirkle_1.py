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
    "jaune": "yellow"
}
NUMBER_OF_EACH_COLOR = 3
NUMBER_OF_COLORS = len(COULEURS)
NUMBER_OF_FORMES = len(FORMES)
NUMBER_OF_PLAYERS = 3
NUMBER_OF_CARDS = 6
COULEUR = "COULEUR"
FORME = "FORME"


def render_hand(hand, separator="\t"):
    print(hand)
    return separator.join([termcolor.colored(FORMES[forme], COULEURS[color]) for forme, color in hand])


def render_board(board):
    print("----------------------")
    print("BOARD :")
    for i, line in enumerate(board):
        print(i, "\t", render_hand(line))
    print("----------------------")


def get_bigger_set_of_cards(hand):
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
    players_sets = []
    for player, hand in players_games.items():
        players_sets.append((player, *get_bigger_set_of_cards(hand)))
    players_sets.sort(key=lambda x: x[3], reverse=True)
    print(players_sets)
    return players_sets[0]


def piocher(hand, pioche):
    cards_to_piocher = 6 - len(hand)
    for i in range(cards_to_piocher):
        hand.append(pioche.pop(0))
    return hand, pioche


def sortir_cartes(hand, selection):
    new_hand = []
    sorties = []
    for i, carte in enumerate(hand):
        if i in selection:
            sorties.append(carte)
        else:
            new_hand.append(carte)
    return new_hand, sorties


def sortir_cartes_selon_couleur(hand, couleur_choisie):
    selection = []
    cartes_selectionnees = []
    for i, (forme, couleur) in enumerate(hand):
        if couleur == couleur_choisie:
            if (forme, couleur) not in cartes_selectionnees:
                selection.append(i)
                cartes_selectionnees.append((forme, couleur))
    return sortir_cartes(hand, selection)


def sortir_cartes_selon_forme(hand, forme_choisie):
    selection = []
    cartes_selectionnees = []
    for i, (forme, couleur) in enumerate(hand):
        if forme == forme_choisie:
            if (forme, couleur) not in cartes_selectionnees:
                selection.append(i)
                cartes_selectionnees.append((forme, couleur))
            selection.append(i)
    return sortir_cartes(hand, selection)


def check_selection_is_ok(hand, selection):
    couleurs = set()
    formes = set()
    for numero in selection:
        formes.add(hand[numero][0])
        couleurs.add(hand[numero][1])
    if len(formes) > 1 and len(couleurs) > 1:
        return False
    else:
        return True


def check_target_is_ok(selection, board_line):
    couleurs = set()
    formes = set()
    for forme, couleur in selection:
        pass


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
    board = [[carte] for carte in cartes]
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
        player_hand = players_games[num_player]
        print("Cartes :", render_hand(player_hand))
        reponse = input("Quelles cartes voulez-vous jouer ? (de 0 à 5, séparé par des virgules)\n")
        liste = [int(i) for i in reponse.replace(" ", "").split(",")]
        if check_selection_is_ok(player_hand, selection=liste):
            player_hand, cartes_a_jouer = sortir_cartes(hand=player_hand,
                                                        selection=liste)
            # Sélectionner la destination







if __name__ == "__main__":
    main()
