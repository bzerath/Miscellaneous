import csv
import datetime
import json
import locale
import matplotlib.pyplot as plt


locale.setlocale(locale.LC_ALL, "")
PATH = r"C:\Users\bzera\PycharmProjects" \
       r"\opencovid19-fr-data\data-sources\sante-publique-france\covid_hospit.csv"


pop_in_each_dpt = {}
with open(r"C:\Users\bzera\PycharmProjects\covid-19\departements-france"
          r"\departements-france-polygons-2020-04-06.json", "r", encoding="utf-8") as datafile:
    data = json.load(datafile)
    for departement in data["features"]:
        prop = departement["properties"]
        pop_in_each_dpt[prop["Code"]] = {"population": prop["Population"]["Total"],
                                         "nom": prop["Province/State"],
                                         "geometry": departement["geometry"].copy(),
                                         "taux_hospitalises": 0,
                                         "taux_reanimation": 0,
                                         "taux_gueris": 0,
                                         "taux_deces": 0,
                                         }

departements = {}

with open(PATH, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")
    for row in reader:
        if row["dep"] not in departements:
            departements[row["dep"]] = {"Tous": {"hospitalises": [],
                                                 "reanimation": [],
                                                 "gueris": [],
                                                 "deces": [],
                                                 "hospitalises_tous": 0,
                                                 "reanimation_tous": 0,
                                                 "gueris_tous": 0,
                                                 "deces_tous": 0,
                                                 },
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

            departements[row["dep"]]["Tous"]["hospitalises_tous"] += int(row["hosp"])
            departements[row["dep"]]["Tous"]["reanimation_tous"] += int(row["rea"])
            departements[row["dep"]]["Tous"]["gueris_tous"] += int(row["rad"])
            departements[row["dep"]]["Tous"]["deces_tous"] += int(row["dc"])
            if row["dep"] in pop_in_each_dpt:
                pop_in_each_dpt[row["dep"]]["taux_hospitalises"] = \
                    departements[row["dep"]]["Tous"]["hospitalises_tous"] \
                    / pop_in_each_dpt[row["dep"]]["population"]
                pop_in_each_dpt[row["dep"]]["taux_reanimation"] = \
                    departements[row["dep"]]["Tous"]["reanimation_tous"] \
                    / pop_in_each_dpt[row["dep"]]["population"]
                pop_in_each_dpt[row["dep"]]["taux_gueris"] = \
                    departements[row["dep"]]["Tous"]["gueris_tous"] \
                    / pop_in_each_dpt[row["dep"]]["population"]
                pop_in_each_dpt[row["dep"]]["taux_deces"] = \
                    departements[row["dep"]]["Tous"]["deces_tous"] \
                    / pop_in_each_dpt[row["dep"]]["population"]
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
        last_date = datetime.datetime.strftime(datetime.datetime.strptime(row["jour"], "%Y-%m-%d"),
                                               "%A %d %B %Y")


compiled_data = {}
plt.subplot(2, 1, 1)
for cas, couleur in (("hospitalises", "black"),
                     ("gueris", "green"),
                     ("reanimation", "orange"),
                     ("deces", "red")):
    compiled_data[cas] = [sum(x) for x in
                          zip(*[data["Tous"][cas]
                                for data in departements.values()
                                if len(data["Tous"][cas]) > 1])]
    plt.plot(range(1, len(compiled_data[cas])+1),
             compiled_data[cas],
             "-",
             label=cas,
             c=couleur)
plt.xlim(1, len(compiled_data["hospitalises"])+1)
plt.title("Malades selon geodes.santepubliquefrance.fr")
plt.legend()

plt.subplot(2, 1, 2)
for cas, couleur in (("hospitalises", "black"),
                     ("gueris", "green"),
                     ("reanimation", "orange"),
                     ("deces", "red")):
    news = []
    for i in range(len(compiled_data[cas])-1):
        news.append(compiled_data[cas][i+1] - compiled_data[cas][i])
    plt.plot(range(2, len(compiled_data[cas])+1),
             news,
             "-",
             label=cas,
             c=couleur)
plt.plot(range(2, len(compiled_data[cas])+1),
         [0]*(len(compiled_data[cas])-1),
         ":",
         c="grey")
plt.title("Nouveaux cas")
plt.xlim(1, len(compiled_data["hospitalises"])+1)
plt.show()

print("En date du {jour}, il y a eu {deces} décès pour {gueris} retours à domicile. "
      "Il y a encore {hospitalisations} hospitalisations en cours "
      "dont {reanimation} en réanimation."
      .format(jour=last_date,
              deces=compiled_data["deces"][-1],
              gueris=compiled_data["gueris"][-1],
              hospitalisations=compiled_data["hospitalises"][-1],
              reanimation=compiled_data["reanimation"][-1],
              ))


geojson = {"type": "FeatureCollection",
           "features": []
           }
for dpt_number, dpt_data in pop_in_each_dpt.items():
    geojson["features"].append({"type": "Feature",
                                "properties": {"population": dpt_data["population"],
                                               "taux_hospitalises": dpt_data["taux_hospitalises"]*100,
                                               "taux_reanimation": dpt_data["taux_reanimation"]*100,
                                               "taux_gueris": dpt_data["taux_gueris"]*100,
                                               "taux_deces": dpt_data["taux_deces"]*100,
                                               "nom": dpt_data["nom"],
                                               "numero": dpt_number,
                                               },
                                "geometry": dpt_data["geometry"]
                                })
with open("departments_taux.json", "w", encoding="utf-8") as output:
    json.dump(geojson, output)
print("(geojson généré avec succès)")

