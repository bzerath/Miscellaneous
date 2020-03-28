
dico_v1 = {
    "f_name": "Duchest",
    "l_name": "Ross",
    "age": 25
}
print("dico_v1", dico_v1)
print()

dico_v2 = dict(f_name="Duchest",
               l_name="Ross",
               age=25)
print("dico_v2", dico_v2)
print()

print("Length of dict dico_v1: ", len(dico_v1))
print("Length of dict dico_v2: ", len(dico_v2))
print()

item_1 = dico_v1["f_name"]
item_2 = dico_v1.get("f_name")
item_3 = dico_v1.get("f_nameeeeee", "Key not found !")
print(item_1, "-", item_2, "-", item_3)
print()

dico_v1["f_name"] = "Duchestttt"
print(dico_v1)
print()

for key in dico_v1:
    print(key)
print()

for key in dico_v1:
    print(dico_v1[key])
print()

for value in dico_v1.values():
    print(value)
print()

for key, value in dico_v1.items():
    print(key, value)
print()

if "f_name" in dico_v1:
    print("Key exists !")
else:
    print("Key does not exist...")
print()

dico_v1["city"] = "Cergy"
print(dico_v1)
dico_v2["city"] = "Cergy"
print(dico_v2)
dico_v1.pop("city")  # Pas forcément recommandé par la doc python
print(dico_v1)
del(dico_v2["city"])
print(dico_v2)
print()

dico_v1["city"] = "Cergy"
dico_v1["city2"] = "Le haut"
print(dico_v1)
dico_v1.popitem()  # Attention : avant python 3.8, enlève un item aléatoire. à éviter.
print(dico_v1)
print()

dico_v1.clear()
print(dico_v1)
print()

dico_v1 = dico_v2
dico_v1["city"] = "Marseille"
print(dico_v1)
print(dico_v2)
print()

dico_v1["city"] = "Cergy"
dico_v1 = dico_v2.copy()
dico_v1["city"] = "Marseille"
print(dico_v1)
print(dico_v2)

group = {
    "person1": {
        "f_name": "Duchest",
        "l_name": "Ross",
        "age": 25
    },
    "person2": {
        "f_name": "Danu",
        "l_name": "Dany",
        "age": 27
    }
}
