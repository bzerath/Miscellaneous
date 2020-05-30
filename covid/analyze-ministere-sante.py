import datetime
import git
import glob
import yaml
import os

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


PATH = r"C:\Users\bzera\PycharmProjects\opencovid19-fr-data"
repo = git.Repo(PATH)
o = repo.remotes.origin
o.pull()

PATH += r"\ministere-sante"


files = glob.glob(os.path.join(PATH, "*.yaml"))

x_axis = []
casConfirmes = []
deces_all = []
deces_hospital = []
decesEhpad = []
hospitalises = []
reanimation = []
gueris = []
casEhpad = []
casConfirmesEhpad = []
casPossiblesEhpad = []

for filepath in files:
    day = os.path.basename(filepath).replace(".yaml", "")
    with open(filepath, "r", encoding='utf-8') as fichier:
        data = yaml.load(fichier, Loader=yaml.CLoader)
        donneesNationales = data["donneesNationales"]

        x_axis.append(datetime.datetime.strptime(day, "%Y-%m-%d"))
        casConfirmes.append(donneesNationales.get("casConfirmes", None))
        deces_hospital.append(donneesNationales.get("deces", None))
        decesEhpad.append(donneesNationales.get("decesEhpad", None))
        deces_all.append(donneesNationales.get("deces", 0) + donneesNationales.get("decesEhpad", 0))
        hospitalises.append(donneesNationales.get("hospitalises", None))
        reanimation.append(donneesNationales.get("reanimation", None))
        gueris.append(donneesNationales.get("gueris", None))
        casEhpad.append(donneesNationales.get("casEhpad", None))
        casConfirmesEhpad.append(donneesNationales.get("casConfirmesEhpad", None))
        casPossiblesEhpad.append(donneesNationales.get("casPossiblesEhpad", None))


fig, ax = plt.subplots()

ax.plot(x_axis,
        deces_hospital,
        "-",
        label="décès (hôpital)",
        c="red")
ax.plot(x_axis,
        decesEhpad,
        "-",
        label="décès (ehpad)",
        c="darkred")
ax.plot(x_axis,
        deces_all,
        ":",
        label="décès (total)",
        c="red")
ax.plot(x_axis,
        hospitalises,
        "-",
        label="hospitalises",
        c="blue")
ax.plot(x_axis,
        reanimation,
        "-",
        label="reanimation",
        c="darkblue")
# ax.plot(x_axis,
#         gueris,
#         ":",
#         label="gueris",
#         c="green")
ax.legend()

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
ax.xaxis.set_minor_locator(mdates.DayLocator())
ax.yaxis.set_major_locator(ticker.MultipleLocator(5000))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(1000))

ax.format_xdata = mdates.DateFormatter('%d-%m-%Y')
ax.grid(b=True, which="major", color="#b0b0b0", linestyle="--")
ax.grid(b=True, which="minor", color="#ddd", linestyle="--")

plt.title("Données selon le ministère de la santé")
plt.gcf().set_size_inches(15, 9)
plt.show()





