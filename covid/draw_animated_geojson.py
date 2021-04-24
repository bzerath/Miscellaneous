import matplotlib; matplotlib.use("TkAgg")

import csv
import os
import git
import glob
import hashlib
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import warnings
from typing import Callable

# Path to cloned repo
PATH = r"C:\Users\bzera\PycharmProjects\CSSEGISandData_COVID-19"
try:
    repo = git.Repo(PATH)
    o = repo.remotes.origin
    o.pull()
except git.exc.GitCommandError as e:
    print(e)
time.sleep(1)

PATH += r"\csse_covid_19_data\csse_covid_19_daily_reports"


def classify_per_property(data: csv.DictReader,
                          prop_name: str,
                          func_filter: Callable[[dict], bool],
                          size_depends_of_func: Callable[[dict], float] = 1) -> dict:
    """ Classify the given geojson basing on given prop_name and return a dict.

    For example, if the prop_name is the country, then the keys of the returning dict will be the
    countries in the geojson.

    func_filter is a function, taking the feature as argument, made to ignore features when this
    filter returns False.

    size_depends_of_func is a function made to change the size of each point depending on something
    in the feature. If not given, default is size = 1.

    :param geojson: geojson as a dict
    :param prop_name: name of the property to classify on
    :param func_filter: filter to ignore features
    :param size_depends_of_func: function to set points' sizes
    :return: dict {prop_name: {"x": [<list of longitudes>],
                               "y": [<list of latitudes>],
                               "sizes": [<list of sizes>]
    """
    output = {}
    for country in data:
        if callable(size_depends_of_func):
            size = size_depends_of_func(country)
        elif isinstance(size_depends_of_func, int):
            size = size_depends_of_func
        else:
            warnings.warn("The given 'size_depends_of_func' argument is not a function nor an int.")
            size = 1
        prop_value = country.get(prop_name) or country.get(prop_name.replace("/", "_"))
        if prop_value not in output:
            output[prop_value] = {"x": [],
                                  "y": [],
                                  "sizes": []}
        geom = float(country.get("Long_", -180) or -180), float(country.get("Lat", -90) or -90)
        if geom[0] == 0 and geom[1] == 0:
            geom = -180, -90
        if func_filter(country):
            output[prop_value]["x"].append(geom[0])
            output[prop_value]["y"].append(geom[1])
            output[prop_value]["sizes"].append(size)
    return output


def get_number_of_cases(feature):
    """ Return number of active cases (confirmed - (deaths+recovered)) """
    confirmed = int(feature["Confirmed"] or 0)
    deaths = int(feature["Deaths"] or 0)
    recovered = int(feature["Recovered"] or 0)
    active = int(feature.get("Active", 0) or 0)
    if feature.get("Combined_Key") == "France":
        print(active if active else confirmed - deaths - recovered)
    try:
        return math.log(active)**3 if active else math.log(confirmed - deaths - recovered)**3
    except ValueError:
        return 0


def animate(filepath):
    """ Return a list of plt.scatter, one for each country in given filepath.

    Called at each iteration of the animation.
    """
    print(filepath)
    scatters = []
    with open(filepath, "r", encoding="utf-8") as fichier:
        data = csv.DictReader(fichier)
        dico = classify_per_property(data,
                                     prop_name="Country/Region",
                                     func_filter=lambda x: int(x["Confirmed"] or 0) > 0,
                                     size_depends_of_func=get_number_of_cases,
                                     )
        for country in dico:
            scatters.append(plt.scatter(x=dico[country]["x"],
                                        y=dico[country]["y"],
                                        s=dico[country]["sizes"],
                                        alpha=0.5,
                                        linewidths=0,
                                        c="#" + hashlib.md5(country.encode()).hexdigest()[:6]))
        return scatters


if __name__ == "__main__":

    # get list of files
    files = glob.glob(os.path.join(PATH, "*.csv"))

    # Initialize figure
    fig = plt.figure()
    scatterplot = plt.scatter([], [])
    # set min/max for x/y to have a beautiful planisphere
    plt.xlim(-180, 180)
    plt.ylim(-90, 90)

    ani = animation.FuncAnimation(fig=fig,
                                  func=animate,
                                  frames=files,
                                  blit=True,
                                  interval=10,
                                  repeat=False)

    plt.gcf().set_size_inches(15, 9)
    plt.show()
