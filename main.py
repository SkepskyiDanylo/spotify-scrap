from dotenv import load_dotenv

import os
import time

from services.api import TokenManager, get_playlist_data, search_for_playlist
from services.files import validate_data, load_links, unique_ids
from services.database import load_to_db


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def load_links_mode(c_id: str, c_secret: str) -> None:
    token_manager = TokenManager(c_id, c_secret)

    while True:
        print("Welcome in load links mode\n"
              "Enter file name\n"
              "File should be in same directory\n"
              "File should be in [txt, csv, xlsx] format\n"
              "If you leave it empty will be used default value('links.txt')'\n"
              "If you want to go back to main menu, type 'q'")
        file_name = input("Enter file name: ")
        clear()

        if file_name == 'q':
            break

        if file_name.strip() == '':
            file_name = 'links.txt'

        result = []
        links_to_check = load_links(file_name.strip())
        if links_to_check:
            for link in links_to_check:
                playlist = get_playlist_data(token_manager, link)
                if playlist:
                    validated = validate_data(playlist)
                    if validated:
                        result.append(validated)
        else:
            time.sleep(2)
            clear()
            continue
        time.sleep(1)
        print(f"Found {len(result)} links out of {len(links_to_check)}")
        print(result)
        input("Press enter to continue")
        if result:
            load_to_db(result)
        else:
            print("Nothing to upload")
        time.sleep(2)
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
        count = 1
        try:
            for i in range(20):
                search_result = search_for_playlist(token_manager, keywords, next_link)
                if search_result:
                    playlists = search_result['items']
                    next_link = search_result["next"]
                    for playlist in playlists:
                        print(f"{count} ", end="")
                        count += 1
                        validated_playlist = validate_data(playlist)
                        if validated_playlist:
                            result.append(validated_playlist)
                            print(validated_playlist)
                else:
                    print("No response or api is down, try again")
                    continue
        except Exception as e:
            print(e)
            input("Press enter to continue")
        clear()
        total = len(result)
        print(f"Found {total} playlists with email out of {count}")
        time.sleep(0.5)
        print(result)
        time.sleep(0.5)
        print("Checking for duplicates:")
        time.sleep(0.5)
        result = [playlist for playlist in result if unique_ids(playlist["link"])]
        print(f"{len(result)} left to upload, {total - len(result)} duplicates removed")
        input("Press enter to upload to db")
        clear()
        if result:
            print(f"Uploading to db")
            time.sleep(1)
            load_to_db(result)
        else:
            print("Nothing to upload")
        time.sleep(2)
        clear()



if __name__ == '__main__':
    load_dotenv()

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    while True:
        print(
            """
            This is a Spotify API service.
            It works in 2 modes:
            1. Loading playlist links from file, and check for email in their description
            2. Looking for playlists by search q (1000 playlists per q)
            Enter 1 or 2, to start working in selected mode
            If You want to exit type 'q' or 'exit' or 'stop'
            """
        )
        command = input("Enter command: ")
        if command in ['q', 'exit', 'stop']:
            break
        elif command == '1':
            clear()
            load_links_mode(client_id, client_secret)
        elif command == '2':
            clear()
            search_mode(client_id, client_secret)
        else:
            print("Invalid command")
            time.sleep(2)
            clear()
