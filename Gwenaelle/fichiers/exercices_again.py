import datetime
import locale
locale.setlocale(locale.LC_ALL, "")

PATH = "noms.txt"

# Parcourt et imprime le fichier sans les sauts de ligne en trop


# Question :
# # "\n" ou "\n\r" --> ?
# # "\t" --> ?


# Trie les noms dans un nouveau fichier


# Ajoute l'heure à la fin
now = datetime.datetime.now().strftime("%A %d %B %Y à %H:%M:%S")
print(now)


# N'affiche que les noms de famille
