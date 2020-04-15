import os
import glob
import json

import matplotlib.pyplot as plt

# Path to cloned repo https://github.com/kalisio/covid-19
PATH = r"C:\Users\bzera\PycharmProjects\covid-19"

PATHS = {"Departements": "departements-france/departements-france-2020*",
         "Regions": "regions-france/regions-france-2020*",
         }

for i, path in enumerate(PATHS):
    files = glob.glob(os.path.join(PATH, PATHS[path]))
    print(files)

    confirmed = []
    severe = []
    critical = []
    deaths = []
    recovered = []

    for json_file_path in sorted(files):
        confirmed_to_sum = []
        severe_to_sum = []
        critical_to_sum = []
        deaths_to_sum = []
        recovered_to_sum = []
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)
            # print(len(json_data["features"]))
            for region in json_data["features"]:
                data = {"name": region["properties"]["Province/State"],
                        "population": region["properties"].get("Population", {}).get("Total", 0),
                        "confirmed": region["properties"].get("Confirmed", 0),
                        "recovered": region["properties"].get("Recovered", 0),
                        "severe": region["properties"].get("Severe", 0),
                        "critical": region["properties"].get("Critical", 0),
                        "deaths": region["properties"].get("Deaths", 0)}
                confirmed_to_sum.append(region["properties"].get("Confirmed", 0))
                severe_to_sum.append(region["properties"].get("Severe", 0))
                critical_to_sum.append(region["properties"].get("Critical", 0))
                deaths_to_sum.append(region["properties"].get("Deaths", 0))
                recovered_to_sum.append(region["properties"].get("Recovered", 0))

        confirmed.append(sum(confirmed_to_sum))
        severe.append(sum(severe_to_sum))
        critical.append(sum(critical_to_sum))
        deaths.append(sum(deaths_to_sum))
        recovered.append(sum(recovered_to_sum))

    plt.subplot(len(PATHS), 1, i+1)
    plt.plot(range(1, len(confirmed)+1),
             confirmed,
             ":",
             color="black",
             label="confirmed")
    plt.plot(range(1, len(severe)+1),
             severe,
             "-",
             color="blue",
             label="severe")
    plt.plot(range(1, len(critical)+1),
             critical,
             "-",
             color="purple",
             label="critical")
    plt.plot(range(1, len(deaths)+1),
             deaths,
             "-",
             color="red",
             label="deaths")
    plt.plot(range(1, len(recovered)+1),
             recovered,
             "-",
             color="green",
             label="recovered")
    plt.title(path)
    plt.legend()
plt.show()
