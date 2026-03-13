"""
Fait par Claude ai
"""

import requests
import sys

QB_URL = "http://localhost:8080"
USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]

YGG_URLS = set()

session = requests.Session()
session.post(f"{QB_URL}/api/v2/auth/login", data={"username": USERNAME, "password": PASSWORD})

torrents = session.get(f"{QB_URL}/api/v2/torrents/info").json()

for torrent in torrents:
    h = torrent["hash"]
    existing = [t["url"] for t in session.get(f"{QB_URL}/api/v2/torrents/trackers", params={"hash": h}).json()]
    for url in existing:
        if "R3QXKTzS9xS6ey1gBZnbPMMCnD4zGWxo" in url:
            YGG_URLS.add(url)

for url in YGG_URLS:
    print(url)


print("Terminé.")