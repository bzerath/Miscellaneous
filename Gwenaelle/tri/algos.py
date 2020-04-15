import random


def selection_sort(tab):
    for i in range(len(tab)):
        min_pos = i
        # Recherche du plus petit élement du reste de la liste
        for j in range(i+1, len(tab)):  # pour chaque élément à droite du pivot
            if tab[j] < tab[min_pos]:   # on checke s'il est le plus petit
                min_pos = j             # si oui, alors on le garde de côté
        tab[i], tab[min_pos] = tab[min_pos], tab[i]  # on permute le plus petit trouvé avec le pivot
    return tab


def bubble_sort(tab):
    swap = True
    n = len(tab)
    while swap:  # tant qu'on a permuté quelque chose
        swap = False
        for i in range(n-1):  # pour chaque élément jusque la fin du tableau
            if tab[i] > tab[i+1]:  # s'il est plus grand que son suivant
                tab[i], tab[i+1] = tab[i+1], tab[i]  # on permute
                swap = True  # on note qu'on a permuté quelque chose, quelque part
        n -= 1
    return tab


def insertion_sort(tab):
    n = len(tab)
    for i in range(1, n):
        j = i
        while j > 0 and tab[j] < tab[j-1]:  # tant qu'il faut faire reculer la valeur
            tab[j], tab[j - 1] = tab[j-1], tab[j]  # on la fait reculer
            j -= 1
    return tab


def cocktail_shaker_sort(tab):
    swap = True
    n = len(tab)
    nb_swaps = 0
    while swap:  # tant qu'on a permuté quelque chose
        nb_swaps += 1
        swap = False
        for i in range(n-1):  # pour chaque élément jusque la fin du tableau
            if tab[i] > tab[i+1]:  # s'il est plus grand que son suivant
                tab[i], tab[i+1] = tab[i+1], tab[i]  # on permute
                swap = True  # on note qu'on a permuté quelque chose, quelque part
        for i in reversed(range(n-1)):  # pour chaque élément jusque le début du tableau
            if tab[i] > tab[i+1]:  # s'il est plus grand que son suivant
                tab[i], tab[i+1] = tab[i+1], tab[i]  # on permute
                swap = True  # on note qu'on a permuté quelque chose, quelque part
        n -= 1
    return tab, nb_swaps


def cocktail_shaker_sort_v2(tab):
    swap = True
    while swap:  # tant qu'on a permuté quelque chose
        swap = False
        for i in range(len(tab) - 1):  # pour chaque élément jusque la fin du tableau
            if tab[i] > tab[i + 1]:  # s'il est plus grand que son suivant
                tab[i], tab[i + 1] = tab[i + 1], tab[i]  # on permute
                swap = True  # on note qu'on a permuté quelque chose, quelque part
        for i in reversed(range(len(tab) - 1)):
            if tab[i] > tab[i + 1]:
                tab[i], tab[i + 1] = tab[i + 1], tab[i]
                swap = True
    return tab


def boolean_sort(tab):
    output = []
    for element in tab:
        if element is True:
            output = output + [element]
        else:
            output = [element] + output
    return output


def french_sort(tab):
    red = []
    white = []
    blue = []
    for color in tab:
        if color == "red":
            red.append(color)
        elif color == "white":
            white.append(color)
        else:
            blue.append(color)
    return blue + white + red


def is_sorted(liste):
    sorted = True
    for i in range(len(liste)-1):
        if liste[i] > liste[i+1]:
            sorted = False
    return sorted


def add_number_to_sorted_list(liste, number):
    liste = [number] + liste
    for i in range(len(liste)-1):
        if liste[i] > liste[i+1]:
            liste[i], liste[i+1] = liste[i+1], liste[i]
    return liste


def bool_array_bis(T):
    current = 0
    end = len(T)-1
    while current < end:
        if T[current] is False:
            current += 1
        else:
            T[current], T[end] = T[end], T[current]
            end -= 1
    return T


def flag(T):
    i_white = len(T)-1
    i_red = len(T)-1
    i_current = 0
    while i_current <= i_red:
        if T[i_current] == "blue":
            i_current += 1
        elif T[i_current] == "red":
            T[i_current], T[i_red] = T[i_red], T[i_current]
            i_red -= 1
        else:
            i_white = i_red - 1
            T[i_current], T[i_red] = T[i_red], T[i_current]
            i_red -= 1
    return T


liste = random.sample(range(11), 11)
print(liste)
# print(bool_array_bis([False, False, True, True, False, True, False, True, False, False]))


print(flag(["red", "white", "blue", "blue", "red", "white", "white", "red", "blue"]))
["red", "white", "blue", "blue", "red", "white", "white", "red", "blue"]  # i_blue=0, i_red=8, current=0


# print(is_sorted(liste.copy()))
# print(is_sorted(sorted(liste.copy())))

# print(add_number_to_sorted_list(sorted(liste.copy()), 6))
# print(add_number_to_sorted_list(sorted(liste.copy()), 0))
# print(add_number_to_sorted_list(sorted(liste.copy()), 10))

# print(cocktail_shaker_sort_v2(liste.copy()))

# print(selection_sort(liste.copy()))
# print(bubble_sort(liste.copy()))
# print(cocktail_shaker_sort(liste.copy()))
# print(insertion_sort(liste.copy()))
# print(boolean_sort([True, False, True, True, False, True, False, True, False, False]))
# print(french_sort(["red", "white", "blue", "blue", "red", "white", "white", "red", "blue"]))
