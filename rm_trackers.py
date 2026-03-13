"""
Fait par Claude ai
"""

import requests
import sys

QB_URL = "http://localhost:8080"
USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]

OLD_TRACKERS = [
    "https://tracker.yggleak.top/announce",
    # Ajoutez vos trackers ici
]

session = requests.Session()
session.post(f"{QB_URL}/api/v2/auth/login", data={"username": USERNAME, "password": PASSWORD})

torrents = session.get(f"{QB_URL}/api/v2/torrents/info").json()

for torrent in torrents:
    h = torrent["hash"]
    try:
        response = session.post(f"{QB_URL}/api/v2/torrents/removeTrackers", data={"hash": h, "urls": "|".join(OLD_TRACKERS)})
        print(response.json())
    except Exception as e:
        print(e, torrent["name"])

print("Terminé.")