import csv
import matplotlib.pyplot as plt

PATH = r"C:\Users\bzera\PycharmProjects" \
       r"\opencovid19-fr-data\data-sources\sante-publique-france\covid_hospit.csv"


departements = {}

with open(PATH, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")
    for row in reader:
        if row["dep"] not in departements:
            departements[row["dep"]] = {"Tous": {"hospitalises": [],
                                                 "reanimation": [],
                                                 "gueris": [],
                                                 "deces": []},
                                        "H": {"hospitalises": [],
                                              "reanimation": [],
                                              "gueris": [],
                                              "deces": []},
                                        "F": {"hospitalises": [],
                                              "reanimation": [],
                                              "gueris": [],
                                              "deces": []}
                                        }
        if row["sexe"] == "0":
            departements[row["dep"]]["Tous"]["hospitalises"].append(int(row["hosp"]))
            departements[row["dep"]]["Tous"]["reanimation"].append(int(row["rea"]))
            departements[row["dep"]]["Tous"]["gueris"].append(int(row["rad"]))
            departements[row["dep"]]["Tous"]["deces"].append(int(row["dc"]))
        if row["sexe"] == "1":
            departements[row["dep"]]["H"]["hospitalises"].append(int(row["hosp"]))
            departements[row["dep"]]["H"]["reanimation"].append(int(row["rea"]))
            departements[row["dep"]]["H"]["gueris"].append(int(row["rad"]))
            departements[row["dep"]]["H"]["deces"].append(int(row["dc"]))
        if row["sexe"] == "2":
            departements[row["dep"]]["F"]["hospitalises"].append(int(row["hosp"]))
            departements[row["dep"]]["F"]["reanimation"].append(int(row["rea"]))
            departements[row["dep"]]["F"]["gueris"].append(int(row["rad"]))
            departements[row["dep"]]["F"]["deces"].append(int(row["dc"]))


for cas, couleur in (("hospitalises", "black"),
                     ("gueris", "green"),
                     ("reanimation", "orange"),
                     ("deces", "red")):
    somme = [sum(x) for x in
             zip(*[data["Tous"][cas]
                   for data in departements.values()
                   if len(data["Tous"][cas]) > 1])]
    plt.plot(range(1, len(somme)+1),
             somme,
             label=cas,
             c=couleur)
plt.legend()
plt.show()

