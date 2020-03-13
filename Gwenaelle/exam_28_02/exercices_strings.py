
def get(mot: str, i: int):
    """ Return element n°`i` in string `mot` """
    if i > len(mot) or i <= 0:
        print("Erreur !")
    else:
        return mot[i-1]


def sub(s: str, position: int, length: int):
    """ Return substring from element `position` of length `length` """
    # Verify that substring will be correct
    if position-1 > len(s) or position-1+length > len(s):
        print("Erreur !",
              position, length, len(s),
              position > len(s),
              len(s) - position < length)
    else:
        substring = ""
        for i in range(position, position+length):
            substring = substring + get(s, i)
        return substring


def reverse(string: str):
    """ Return the string reversed """
    reversed_string = ""
    for i in range(len(string)):
        reversed_string = string[i] + reversed_string
    return reversed_string


def appears(string: str, item: str):
    """ Return whether `item` is in `string` """
    check = False
    for i in range(1, len(string)+1):
        if get(string, i) == item:
            check = True
    return check


def count(string: str, item: str):
    """ Return the number of occurrences of `item` in `string` """
    compteur = 0
    for i in range(1, len(string)+1):
        if get(string, i) == item:
            compteur += 1
    return compteur


def index(string: str, item: str):
    """ Return first occurrence of `item` in `string` """
    index_ = 0
    for i in range(1, len(string)+1):
        if get(string, i) == item:
            index_ = i-1
            break
        else:
            index_ = -1
    return index_


def last_index(string: str, item: str):
    """ Return last occurrence of `item` in `string` """
    index_ = 0
    reversed_string = reverse(string)
    for i in range(1, len(reversed_string)+1):
        if get(reversed_string, i) == item:
            index_ = len(reversed_string) - i
            break
        else:
            index_ = -1
    return index_


def index_from(string: str, item: str, position_from: int):
    """ Return index of `item` in `string` from position `position_from` """
    index_ = 0
    for i in range(position_from, len(string)+1):
        if get(string, i) == item:
            index_ = i-1
            break
        else:
            index_ = -1
    return index_


def split(string: str, sep: str):
    """ Return a list of the words in the string, using sep as the delimiter string """
    output = []  # Prepare output

    temp_string = ""  # prepare temporary string
    for i in range(len(string)):  # iterate on string
        lettre = string[i]
        if lettre != sep:  # if the letter found IS NOT `sep`
            temp_string += lettre  # we can keep it in the current temp_string
        elif lettre == sep:
            output.append(temp_string)  # else: store the temp_string
            temp_string = ""
    output.append(temp_string)

    return output


def join(liste: list, sep: str):
    output_string = ""
    for i in range(len(liste)-1):
        output_string += liste[i] + sep
    output_string += liste[-1]

    return output_string


def stat(string: str):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    output = []

    for letter in alphabet:
        output.append((letter, count(string, letter)))

    return output


if __name__ == "__main__":

    print(join(['hello', 'world', 'welcome', 'to', 'my', 'life'], sep=","))

    print(stat("hello,world,welcome,to,my,life"))

    # print("get", get("hello", 2))
    # print("get", get("hello", -1))
    # print("get", get("hello", 1000))
    #
    # print()
    #
    # print("sub", sub("hello", position=2, length=3))   # ell
    # print("sub", sub("hello", position=4, length=1))   # l
    # print("sub", sub("hello", position=5, length=1))   # o
    # print("sub", sub("hello", position=6, length=1))   # crash
    # print("sub", sub("hello", position=3, length=10))  # crash
    #
    # print()
    #
    # print("reverse", reverse("hello"))
    #
    # print()
    #
    # print("appears1", appears("hello", "l"))
    # print("appears2", appears("hello", "z"))
    #
    # print()
    #
    # print("count1", count("hello", "l"))
    # print("count2", count("hello", "z"))
    #
    # print()
    #
    # print("index1", index("hello", "l"))
    # print("index1", index("hello", "z"))
    #
    # print()
    #
    # print("last_index", last_index("hello", "l"))  # 3
    # print("last_index", last_index("hello", "z"))  # -1
    #
    # print()
    #
    # print("index_from", index_from("hello world hey hey", item="h", position_from=5))  # 12
    #
    # print()
    #
    # print(split("hello,world,welcome,to,my,life", ","))
    #
    # print()

