import termcolor

FORMES = {
    "croix": "X",
    "losange": "♦",
    "cercle": "●",
    "carré": "■",
    "étoile": "☼",
    "trèfle": "♣"
}
COULEURS = {
    "rouge": "red",
    "violet": "magenta",
    "bleu": "blue",
    "orange": "white",  # pas d'orange en console
    "vert": "green",
    "jaune": "yellow"
}

print("Couleurs disponibles :", ", ".join(termcolor.COLORS.keys()))

for color, code_color in COULEURS.items():
    print("{}\t{}".format(color,
                          termcolor.colored("".join(FORMES.values()),
                                            code_color)
                          )
          )
