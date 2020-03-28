"""
question 2 :
 - soit créer un nouveau dict en contrôlant chaque ajout voir s'il n'est pas déjà présent
 - soit parcourir chaque personne, créer une liste des personnes déjà vues. et si une personne a déjà été croisée, del(la personne)

question 3 :
 - idem

question 4:
 analyse standard de dico.
 faire un dico avec des tuples (entreprise, ville) pour les résultats
"""

import random
from datetime import datetime, timedelta
from pprint import pprint


people_names = ["Taliah Villegas",
                "Lea Carroll",
                "Johnathon Andrade",
                "Letitia Shannon",
                "Cavan Davies",
                "Khadijah Pittman",
                "Terrence O'Connor",
                "Kyle Peters",
                "Hasan Sweeney",
                "Jay-Jay Fuller",
                "Anne-Marie Grimes",
                "Isla-Grace Marks",
                "Mary O'Moore",
                "Sayed Chandler",
                "Hamid Laing",
                "Harriet Montes",
                "India Peterson",
                "Aalia Huffman",
                "Christiana Rubio",
                "Louie Turnbull",
                "Niamh Broadhurst",
                "Mayson Cabrera",
                "Jaxon Figueroa",
                "Carlos Sexton",
                "Caitlin Traynor",
                "Colm Chadwick",
                "Nabeela Francis",
                "Kathleen Atkinson",
                "Rebecca Philip",
                "Musab Berger",
                ]

enterprise_names = ["Corona 19",
                    "Luther corp",
                    "Carrefour",
                    "Isaac Enterprise",
                    "Sony",
                    "Cookie Clicker",
                    "Bose",
                    "Capsule Corp",
                    ]

cities_names = ["Bourg Palette",
                "Paris",
                "Maisons-Alfort",
                "San Fransokyo"]

jobs = ["Ingénieur(e)",
        "Agent(e) de ménage",
        "Docteur(e)",
        "Designer(e)",
        "Enquêteur(trice)",
        "Secrétaire médical(e)",
        "Instituteur(trice)",
        "Conducteur(trice) de car"
        ]


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


d1 = datetime.strptime('01/01/2018', '%d/%m/%Y')
d2 = datetime.strptime('14/03/2020', '%d/%m/%Y')

dico = {}
# Create 30 peoples
for i in range(len(people_names)):
    dico[i] = {"name": people_names[i],
               "age": random.randint(18, 67),
               "city": random.choice(cities_names),
               "job": random.choice(jobs),
               "company": random.choice(enterprise_names),
               "date": random_date(d1, d2).strftime('%d/%m/%Y')}

# Volontary create 10 duplicates
begin = len(dico.keys())
for i in range(10):
    dico[begin+i] = {"name": random.choice(people_names),
                     "age": random.randint(18, 67),
                     "city": random.choice(cities_names),
                     "job": random.choice(jobs),
                     "company": random.choice(enterprise_names),
                     "date": random_date(d1, d2).strftime('%d/%m/%Y')}

# Volontary duplicate the #1 person
dico[max(dico.keys())+1] = dico[0].copy()

pprint(dico)
