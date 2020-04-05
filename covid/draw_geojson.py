import os
import json
import math
import matplotlib.pyplot as plt

PATH = r"/csse_covid_19_daily_reports"


def classify_per_property(geojson, prop_name, func_filter, size_depends_of_func=None):
    output = {}
    for feature in geojson["features"]:
        size = size_depends_of_func(feature)
        prop_value = feature["properties"][prop_name]
        if prop_value not in output:
            output[prop_value] = {"x": [],
                                  "y": [],
                                  "size_depends_of": []}
        geom = feature["geometry"]
        if geom["type"] == "Point" and func_filter(feature):
            output[prop_value]["x"].append(geom["coordinates"][0])
            output[prop_value]["y"].append(geom["coordinates"][1])
            output[prop_value]["size_depends_of"].append(size)
    return output


if __name__ == "__main__":

    with open(os.path.join(PATH, "csse_covid_19_daily_report_03-25-2020.json"), "r", encoding="utf-8") as fichier:
        data = json.load(fichier)
        print(len(data["features"]))

    dico = classify_per_property(data,
                                 prop_name="Country/Region",
                                 func_filter=lambda x: int(x["properties"]["Confirmed"]) > 0,
                                 # size_depends_of_func=lambda x: math.log(int(x["properties"]["Confirmed"]))*5 if int(x["properties"]["Confirmed"]) > 0 else 0,
                                 size_depends_of_func=lambda x: int(x["properties"]["Confirmed"])/10,
                                 )
    # for country in dico:
    #     print(country, len(dico[country]["x"]), len(dico[country]["y"]))

    plt.xlim(-180, 180)
    plt.ylim(-90, 90)
    for country in dico:
        plt.scatter(x=dico[country]["x"],
                    y=dico[country]["y"],
                    s=dico[country]["size_depends_of"],
                    alpha=0.5,
                    linewidths=0)
    plt.gcf().set_size_inches(15, 9)
    plt.show()


