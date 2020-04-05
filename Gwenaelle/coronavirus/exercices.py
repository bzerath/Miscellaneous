import json
import pprint

PATH = r"C:\Users\bzera\PycharmProjects\covid-19\regions-france\regions-france-2020-04-02.json"
dico = {}

with open(PATH, "r", encoding="utf-8") as json_file:
    data_in_json = json.load(json_file)
    list_of_features = data_in_json["features"]
    print("Il y a", len(list_of_features), "régions dans ce fichier.")
    for region in list_of_features:
        proprietes = region["properties"]
        # "<nom de la région> : Confirmés=<nb>, Morts=<nb>, Soignés=<nb>"
        # print(proprietes["Province/State"], ":",
        #       "confirmés =", proprietes.get("Confirmed", 0),
        #       "Morts =", proprietes.get("Deaths", 0),
        #       "soignés =", proprietes.get("Recovered", 0)
        #       )
        dico[proprietes["Province/State"]] = {"confirmés": proprietes.get("Confirmed", 0),
                                              "morts": proprietes.get("Deaths", 0),
                                              "soignés": proprietes.get("Recovered", 0)}
# pprint.pprint(dico)

delimiter = ";"
with open("regions.csv", "w", encoding='latin-1') as fichier:
    header = delimiter.join(["Région", "Confirmés", "Morts", "Soignés\n"])
    fichier.write(header)
    for region_name in dico:
        fichier.write(region_name + delimiter +
                      str(dico[region_name]["confirmés"]) + delimiter +
                      str(dico[region_name]["morts"]) + delimiter +
                      str(dico[region_name]["soignés"]) + "\n")
