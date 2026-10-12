import os
import qbittorrentapi
from dotenv import load_dotenv, dotenv_values

load_dotenv()

# instantiate a Client using the appropriate WebUI configuration
conn_info = dict(
    host=os.getenv("HOST"),
    port=os.getenv("PORT"),
    username=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
)

qbt_client = qbittorrentapi.Client(**conn_info)

# the Client will automatically acquire/maintain a logged-in state
# in line with any request. therefore, this is not strictly necessary;
# however, you may want to test the provided login credentials.
try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

# if the Client will not be long-lived or many Clients may be created
# in a relatively short amount of time, be sure to log out:

# qbt_client.auth_log_out()

# or use a context manager:

# with qbittorrentapi.Client(**conn_info) as qbt_client:
#   if qbt_client.torrents_add(urls="...") != "Ok.":
#        raise Exception("Failed to add torrent.")

# Hash and path
possible_torrents: dict[str, tuple[str, str, bool]] = {}
# retrieve and show all torrents
for torrent in qbt_client.torrents_info():
    if torrent.amount_left > 0:
        continue
    if "anna/download" in torrent.content_path:
        continue
    if "/torrent_data" in torrent.content_path:
        continue

    possible_torrents[torrent.hash] = (
        torrent.name,
        torrent.content_path,
        torrent.private,
    )

with open("temp.txt", "w", encoding="utf-8") as f:
    for torrent in possible_torrents.values():
        f.write(f"{torrent[1]}\n")