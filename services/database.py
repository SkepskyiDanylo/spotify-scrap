import sqlite3


class SpotifyDatabase:
    def __init__(self):
        self._connection = sqlite3.connect("spotify_emails.sqlite")
        self._table_name = "data"

    def create(self, name: str, email: str, link: str, song_type: str) -> str:
        self._connection.execute(
            f"INSERT INTO {self._table_name} "
            f"(name, email, link, type) VALUES (?, ?, ?, ?)",
            (name, email, link, song_type)
        )
        self._connection.commit()


def load_to_db(data: list) -> None:
    database = SpotifyDatabase()
    count = 0
    song_type = input("Enter the type of songs: ")
    for count, playlist in enumerate(data):
        try:
            database.create(playlist["name"], playlist["email"], playlist["link"], song_type)
            print(f"Successfully uploaded{playlist['name']}")
        except Exception as e:
            print(f"Error: {e} for playlist {playlist['name']}")
    print(f"Successfully uploaded {count + 1} playlists")