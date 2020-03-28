from pprint import pprint


def exo1():
    digit_as_string = {
        "1": "One",
        "2": "Two",
        "3": "Three",
        "4": "Four",
        "5": "Five",
        "6": "Six",
        "7": "Seven",
        "8": "Eight",
        "9": "Nine",
        "0": "Zero"
    }
    print("Number ?")
    number = input()
    output = ""
    for digit in number:
        output = output + digit_as_string[digit] + " "
    print(output)


def exo1():
    output = ""
    nombre = input("Nombre ?")
    digit_as_string = {
        "1": "One",
        "2": "Two",
        "3": "Three",
        "4": "Four",
        "5": "Five",
        "6": "Six",
        "7": "Seven",
        "8": "Eight",
        "9": "Nine",
        "0": "Zero"
    }
    for i in range(len(nombre)):
        current_digit = nombre[i]
        output = output + digit_as_string[current_digit] + " "
    print(output)


def exo2(keys: list, values: list):
    output = {}
    for i in range(len(keys)):
        output[keys[i]] = values[i]
    return output


def exo2_v1(keys: list, values: list):
    output = {}
    for i in range(len(keys)):
        output[keys[i]] = values[i]
    return output


def exo2_v2(keys: list, values: list):
    output = {}
    for key, value in zip(keys, values):
        output[key] = value
    return output


def exo3(dict1: dict, dict2: dict):
    # Voir aussi : dico.update(dico2), conditions de merge...
    output = dict1.copy()
    for key, value in dict2.items():
        output[key] = value
    return output


def exo3(dict1: dict, dict2: dict):
    """
    Choix de conception :
     - en cas de conflit --> erreur
     - on crée un 3e dico sans modifier les 2 premiers

    :param dict1:
    :param dict2:
    :return:
    """
    output = {}
    for key in dict1:
        if key in dict2:
            print("Error: the key '{}' is in dict1 and dict2 !".format(key))
            return
    for key in dict1:
        output[key] = dict1[key]
    for key in dict2:
        output[key] = dict2[key]

    # pass --> Ne rien faire
    # break --> casse la boucle dans laquelle on est. N'impacte pas une imbrication de boucles.
    # continue --> passe à l'itération suivante
    # return --> quitte la fonction en renvoyant la valeur donnée, None si aucune valeur n'est donnée (= return None)
    return output


if __name__ == "__main__":
    pass
    # exo1()
    # print(exo2(["ten", "Twenty", "Thirty"],
    #            [10, 20, 30]))
    # print(exo2_v2(["ten", "Twenty", "Thirty"],
    #               [10, 20, 30]))
    dict1 = {'f_name': 'Duchest', 'l_name': 'Ross', 'age': 25}
    dict2 = {'ten': 10, 'Twenty': 20, 'Thirty': 30, 'age': 42}
    pprint(exo3(dict1=dict1,
                dict2=dict2))
    print(dict1, "\n", dict2)
