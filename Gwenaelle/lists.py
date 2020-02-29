def shift_v1(liste_to_shift, index_item, decalage):
    return (liste_to_shift[0:index_item] +
            liste_to_shift[index_item + 1:index_item + 1 + decalage] +
            [liste_to_shift[index_item]] +
            liste_to_shift[index_item + 1 + decalage:]
            )


def shift_v2(liste_to_shift, index_item, decalage):
    _item = liste_to_shift[index_item]
    liste_to_shift.pop(index_item)
    liste_to_shift.insert(index_item + decalage, _item)
    return liste_to_shift


def count_longest_1(liste_to_count):
    curr_length = 0
    max_length = 0
    index_max_length = 0
    index_curr_length = 0
    we_are_in_a_set_of_1 = False
    for i in range(len(liste_to_count)):
        if liste_to_count[i] == 0:
            we_are_in_a_set_of_1 = False
            if curr_length > max_length:
                max_length = curr_length
                index_max_length = index_curr_length
        elif liste_to_count[i] == 1 and we_are_in_a_set_of_1 is False:
            we_are_in_a_set_of_1 = True
            curr_length = 1
            index_curr_length = i
        elif liste_to_count[i] == 1 and we_are_in_a_set_of_1 is True:
            curr_length += 1
    if curr_length > max_length:
        max_length = curr_length
        index_max_length = index_curr_length
    return index_max_length, max_length



if __name__ == "__main__":
    liste = ["a", "b", "c", "d", "e", "f", "g", "h"]
    liste_bin = [0, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                 0, 0, 1, 0, 1, 1, 1, 0, 0, 0,
                 1, 1, 1, 1, 1, 0, 0, 1, 0, 1,
                 0, 1, 1, 0, 1, 0, 0, 0, 1, 1,
                 1, 0, 0, 0, 0, 1, 1, 1, 1, 0]

    liste_bin_2 = [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0]


    print(shift_v1(liste, 2, 2))
    print(shift_v2(liste, 2, 2))

    print(count_longest_1(liste_bin))
    print(count_longest_1(liste_bin_2))
