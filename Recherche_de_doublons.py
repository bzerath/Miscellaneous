import os
from datetime import datetime


def convert_date(timestamp):
    d = datetime.fromtimestamp(timestamp)
    formated_date = d.strftime('%d/%m/%Y %H:%M:%S')
    return formated_date


def clean_doublons(dossier_source, photo1, photo2):
    stats1 = os.stat(dossier_source + "\\" + photo1)
    creation1 = stats1.st_mtime
    size1 = stats1.st_size

    stats2 = os.stat(dossier_source + "\\" + photo2)
    creation2 = stats2.st_mtime
    size2 = stats2.st_size

    if creation1 == creation2 and size1 == size2:
        print(photo1, "-", convert_date(creation1), "-", round(size1 / 1024), "ko")
        print(photo2, "-", convert_date(creation2), "-", round(size2 / 1024), "ko")
        print("Removing ", photo2)
        os.remove(dossier_source + "\\" + photo2)


if __name__ == "__main__":
    # dossier = r"C:\Users\bzera\OneDrive\Images\Saved Pictures"
    dossier = r"\\Synology_DS215J\photo\Sauvegarde auto"
    fichiers = [image for image in os.listdir(dossier)
                if image.lower().endswith("jpg")
                and "BURST" not in image
                and "FB_IMG" not in image
                ]
    print(len(fichiers))

    photos = {}

    for fichier in fichiers:
        nom_reduit = fichier[:9]
        if nom_reduit not in photos:
            photos[nom_reduit] = []
        photos[nom_reduit].append(fichier)

    fichiers_quasi_meme_noms = list(photos.keys())[:]
    for photo in fichiers_quasi_meme_noms:
        if len(photos[photo]) < 2:
            del(photos[photo])

    print(len(fichiers_quasi_meme_noms), "-->", len(photos))

    for photos_ptet_en_double in photos:
        if len(photos[photos_ptet_en_double]) > 2:
            for photo in photos[photos_ptet_en_double]:
                stats = os.stat(dossier + "\\" + photo)
                print(photo, "-", convert_date(stats.st_mtime), "-", round(stats.st_size / 1024), "ko")
            print("")
            try:
                clean_doublons(dossier, photos[photos_ptet_en_double][1], photos[photos_ptet_en_double][2])
            except:
                pass
