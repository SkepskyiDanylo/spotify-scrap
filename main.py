import init_django_orm  # noqa: E402
import os

from dotenv import load_dotenv
from time import sleep, time

from db.models import Playlist, Track
from lib.api import (TokenManager,
                     get_playlist_data,
                     get_track_data,
                     search_for_playlist,
                     validate_playlist)
from lib.files import (FileManager,
                       get_used_data,
                       upload_used_data,
                       check_for_duplicates)


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def load_top_tracks(c_id: str, c_secret: str) -> None:
    token_manager = TokenManager(c_id, c_secret)
    data = get_used_data()
    last_id = data["last_playlist_id"]
    playlists = Playlist.objects.filter(id__gt=last_id).values("id", "link")
    for playlist in playlists:
        tracks = get_track_data(token_manager=token_manager,
                                playlist_link=playlist["link"])
        for place, track in enumerate(tracks):
            name = track[0]
            author = track[1]
            popularity = track[2]
            link = track[3]
            Track.objects.create(
                name=name,
                author=author,
                popularity=popularity,
                link=link,
                place=place + 1,
                playlist_id=playlist["id"],
            )
    data["last_playlist_id"] = list(playlists)[-1]["id"]
    upload_used_data(data)


def load_links_mode(c_id: str, c_secret: str) -> None:
    token_manager = TokenManager(c_id, c_secret)
    file_manager = FileManager()
    while True:
        start = time()
        print("Welcome in load links mode\n"
              "Loading files from 'files' folder, "
              "please move files you want to check there\n"
              "Possible formats: .txt, .csv, .xlsx\n"
              "To exit type 'q'")
        com = input("Press enter or type 'q': ")
        if com == "q":
            break
        else:
            ids = file_manager.load_folder()
            if ids:
                song_type = input("Enter the playlist type:")
                for p_id in ids:
                    playlist = get_playlist_data(token_manager=token_manager,
                                                 playlist_id=p_id)
                    if playlist:
                        name = playlist.get("name")
                        email = playlist.get("email")
                        link = playlist.get("link")
                        print(f"Uploading {name}")
                        Playlist.objects.create(name=name,
                                                email=email,
                                                link=link,
                                                song_type=song_type)
                load_top_tracks(c_id=c_id, c_secret=c_secret)
            else:
                print("No playlists found")
                clear()
                continue
        end = time()
        print(f"It took {end - start} seconds")
        sleep(2)
        clear()


def search_mode(c_id: str, c_secret: str) -> None:
    token_manager = TokenManager(c_id, c_secret)

    while True:
        print("Welcome in search mode\n"
              "Enter your search query or 'q' to go back to main menu")
        keywords = input("Search q: ")

        if keywords == "q":
            clear()
            break
        keywords = keywords.strip()
        result = []
        next_link = None
        count = 0
        for _ in range(20):
            try:
                search_result = search_for_playlist(token_manager, keywords, next_link)
                if search_result:
                    playlist = search_result["items"]
                    next_link = search_result["next"]
                    for playlist in playlist:
                        count += 1
                        print(f"{count}", end="")
                        validated = validate_playlist(playlist)
                        if validated:
                            result.append(validated)
            except Exception as e:
                print("Some error there", e)
                return
        clear()
        print(f"Total playlist count: {len(result)}, out of {count}")
        result = [result for result in result if check_for_duplicates(result["link"])]
        if result:
            song_type = input("Enter the playlist type: ")
            for playlist in result:
                name = playlist.get("name")
                email = playlist.get("email")
                link = playlist.get("link")
                print(f"Uploading {name}")
                Playlist.objects.create(name=name,
                                        email=email,
                                        link=link,
                                        song_type=song_type)
            load_top_tracks(c_id=c_id, c_secret=c_secret)
        else:
            print("No playlists")
        clear()


if __name__ == '__main__':
    try:
        load_dotenv(os.path.join("assets", ".env"))
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")

        while True:
            print("""
            This is a Spotify API service.
            It works in 2 modes:
            1. Loading playlist links from file, and check for email in their description
            2. Looking for playlists by search q (<1000 playlists per q)
            Enter 1 or 2, to start working in selected mode
            If You want to exit type 'q'
            """
                  )

            command = input("Enter command: ")

            if command == "q":
                break
            elif command == "1":
                clear()
                load_links_mode(client_id, client_secret)
            elif command == "2":
                clear()
                search_mode(client_id, client_secret)
            else:
                print("Invalid command")
                sleep(1)
                clear()

    except KeyboardInterrupt:
        clear()
        print("\nShutting down")
        sleep(1)
    except Exception as e:
        print("Unexpected error:", e)
        sleep(5)
        input("Press enter to exit")
