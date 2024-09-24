import sqlite3


class SpotifyDatabase:
    def __init__(self):
        self._connection = sqlite3.connect("spotify_db.sqlite")
        self._table_name = "playlists"

    def create(self, name: str, email: str, link: str, song_type: str) -> str:
        self._connection.execute(
            f"INSERT INTO {self._table_name} "
            f"(name, email, link, type) VALUES (?, ?, ?, ?)",
            (name, email, link, song_type)
        )
        self._connection.commit()

    def get(self) -> list[str]:
        cursor = self._connection.execute(
            f"SELECT id, link FROM {self._table_name} "
        )
        return [(link[0], link[1]) for link in cursor]


class TrackDatabase:
    def __init__(self):
        self._connection = sqlite3.connect("spotify_db.sqlite")
        self._table_name = "top_tracks"

    def create(self, playlist_id: str,
               name: str, artist: str,
               popularity: int,
               place: int,
               link: str) -> str:
        self._connection.execute(
            f"INSERT INTO {self._table_name} "
            f"(playlist_id, name, popularity, place, link, author) "
            f"VALUES (?, ?, ?, ?, ?, ?)",
            (playlist_id, name, popularity, place, link, artist)
        )
        self._connection.commit()


def load_to_db(data: list, type_of_object: str) -> None:
    if type_of_object == "playlist":
        database = SpotifyDatabase()
        count = 0
        song_type = input("Enter the type of songs: ")
        for count, playlist in enumerate(data):
            try:
                database.create(playlist["name"],
                                playlist["email"],
                                playlist["link"], song_type)
                print(f"Successfully uploaded{playlist['name']}")
            except Exception as e:
                print(f"Error: {e} for playlist {playlist['name']}")
        print(f"Successfully uploaded {count + 1} playlists")
    elif type_of_object == "track":
        database = TrackDatabase()
        for playlist in data:
            for place, track in enumerate(playlist[1]):
                try:
                    database.create(
                        playlist_id=playlist[0],
                        name=track[0],
                        artist=track[1],
                        popularity=track[2],
                        link=track[3],
                        place=place + 1)
                except Exception as e:
                    print(f"Error: {e}")


def get_from_db() -> list[str]:
    database = SpotifyDatabase()
    return database.get()
