import glob
import json

PATH = r"C:\Users\bzera\PycharmProjects\covid-19\regions-france\regions-france-2020-04-13.json"
CSSE_FILEPATH = r"C:\Users\bzera\PycharmProjects\covid-19\csse_covid_19_daily_reports\csse_covid_19_daily_report_04-14-2020.json"


# Créer un dictionnaire qui associe à chaque région ("Province/State") les confirmés, les morts, et les soignés


# Exporter ça dans un fichier CSV manuellement : Département;Confirmés;Morts;Guéris;


# Exporter ça dans un fichier CSV en utilisant csv.dictwriter


# Ouvrir le fichier CSSE_FILEPATH et afficher toutes les informations concernant la France métropolitaine


# Ouvrir le fichier CSSE_FILEPATH et n'afficher que les confirmés, morts et soignés concernant la France métropolitaine


# Ceci est la liste des fichiers depuis début mars
liste_des_fichiers = glob.glob(r"C:\Users\bzera\PycharmProjects\covid-19\csse_covid_19_daily_reports\*.json")
# Afficher les confirmés, morts et soignés concernant la France métropolitaine pour chaque fichier successivement


# Extraire ces données sous la forme d'un CSV avec csv.dictwriter (Date;confirmés;décès;guéris;)
