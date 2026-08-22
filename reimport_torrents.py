"""
Réimport en masse de fichiers .torrent dans qBittorrent après réinstallation,
en retrouvant automatiquement le bon dossier de données (hardlinks cross-seed
ou bibliothèque *arr) grâce au nom stocké dans chaque .torrent.

Principe : on ne re-télécharge rien. On pointe chaque torrent vers un dossier
existant contenant déjà les bonnes données, puis on force un recheck complet
(skip_checking=false) pour laisser qBittorrent valider lui-même les hash.
"""

import os
import bencodepy
import requests

# --- À ADAPTER ---
QBIT_URL = "http://localhost:8080"
USERNAME = "admin"
PASSWORD = "adminadmin"

TORRENT_DIR = r"C:\chemin\vers\tes_fichiers_torrent"
SEARCH_ROOT = r"D:\chemin\vers\racine_des_telechargements"  # doit englober bibliothèque + linkDir cross-seed
# ------------------

session = requests.Session()


def login():
    r = session.post(f"{QBIT_URL}/api/v2/auth/login",
                      data={"username": USERNAME, "password": PASSWORD})
    r.raise_for_status()
    if r.text != "Ok.":
        raise RuntimeError("Échec de connexion à qBittorrent (identifiants ?)")


def get_torrent_root_name(torrent_path):
    with open(torrent_path, "rb") as f:
        data = bencodepy.decode(f.read())
    info = data[b"info"]
    return info[b"name"].decode("utf-8", errors="replace")


def build_name_index(root):
    """Indexe nom -> liste des dossiers parents où ce nom apparaît (fichier ou dossier)."""
    index = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for d in dirnames:
            index.setdefault(d, []).append(dirpath)
        for f in filenames:
            index.setdefault(f, []).append(dirpath)
    return index


def add_torrent(torrent_path, savepath):
    with open(torrent_path, "rb") as f:
        files = {"torrents": (os.path.basename(torrent_path), f, "application/x-bittorrent")}
        data = {
            "savepath": savepath,
            "autoTMM": "false",
            "skip_checking": "false",  # recheck forcé, volontairement, ne pas faire confiance au matching par nom
            "paused": "false",
        }
        r = session.post(f"{QBIT_URL}/api/v2/torrents/add", data=data, files=files)
        r.raise_for_status()


def main():
    login()
    index = build_name_index(SEARCH_ROOT)
    unmatched, ambiguous = [], []

    for fname in sorted(os.listdir(TORRENT_DIR)):
        if not fname.endswith(".torrent"):
            continue
        tpath = os.path.join(TORRENT_DIR, fname)
        try:
            root_name = get_torrent_root_name(tpath)
        except Exception as e:
            print(f"[ERREUR décodage] {fname}: {e}")
            continue

        matches = index.get(root_name)
        if not matches:
            unmatched.append(fname)
            continue
        if len(matches) > 1:
            ambiguous.append((fname, matches))

        savepath = matches[0]  # même contenu quel que soit le hardlink choisi
        try:
            add_torrent(tpath, savepath)
            print(f"[OK] {fname} -> {savepath}")
        except Exception as e:
            print(f"[ÉCHEC injection] {fname}: {e}")

    print(f"\n{len(unmatched)} torrent(s) sans correspondance trouvée :")
    for u in unmatched:
        print(f"  - {u}")

    print(f"\n{len(ambiguous)} torrent(s) avec correspondances multiples (premier chemin utilisé) :")
    for fname, matches in ambiguous:
        print(f"  - {fname}: {matches}")


if __name__ == "__main__":
    main()