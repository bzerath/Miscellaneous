"""
Fait par Claude ai
"""

import requests
import sys

QB_URL = "http://localhost:8080"
USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]

NEW_TRACKERS = [
    "https://tracker.yggleak.top/announce",
    # Ajoutez vos trackers ici
]

session = requests.Session()
session.post(f"{QB_URL}/api/v2/auth/login", data={"username": USERNAME, "password": PASSWORD})

torrents = session.get(f"{QB_URL}/api/v2/torrents/info").json()

for torrent in torrents:
    h = torrent["hash"]
    existing = [t["url"] for t in session.get(f"{QB_URL}/api/v2/torrents/trackers", params={"hash": h}).json()]
    to_add = [t for t in NEW_TRACKERS if t not in existing]
    if to_add:
        session.post(f"{QB_URL}/api/v2/torrents/addTrackers", data={"hash": h, "urls": "\n".join(to_add)})
        print(f"Trackers ajoutés à : {torrent['name']}")

print("Terminé.")