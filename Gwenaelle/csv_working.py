def get_language(ligne):
    ligne_parsee = ligne.split("\t")
    return ligne_parsee[1]


with open("sentences.csv", "r", encoding="utf-8") as input:
    with open("sentences_fra_eng.csv", "w", encoding="utf-8") as output:
        ligne = input.readline()
        while ligne != "":
            if get_language(ligne) in ("eng", "fra"):
                output.write(ligne)
            ligne = input.readline()

# with open("sentences_fra_eng.csv", "r", encoding="utf-8") as new_input:
#     i = 0
#     ligne = new_input.readline()
#     while ligne != "":
#         i += 1
#         if i == 10:
#             break
#         print(ligne)
#         ligne = new_input.readline()
#
