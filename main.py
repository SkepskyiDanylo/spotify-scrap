from dotenv import load_dotenv
import os
import time

from services.api import get_token, get_playlist_data, search_for_playlist, next_playlist
from services.files import validate_data, load_links, write_file, get_used_data


if __name__ == '__main__':
    load_dotenv()

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    # ids = load_urls("urls.txt")
    # if ids:
    #     token = get_token(client_id, client_secret)
    #     result = []
    #     for id in ids:
    #         data = get_playlist_data(token, id)
    #         validated_data = validate_data(data)
    #         if validated_data:
    #             result.append(validated_data)
    #     write_file(result)
    # else:
    #     print("No new urls found!")

    keyword = input("Enter search term: ")
    result = []
    start = time.time()
    token = get_token(client_id, client_secret)
    search_result = search_for_playlist(token, keyword.strip())
    playlists = search_result["items"]
    next_link = search_result["next"]
    count = 1
    for playlist in playlists:
        print(f"{count} ", end="")
        count += 1
        validated_playlist = validate_data(playlist)
        if validated_playlist:
            print(validated_playlist)
    for _ in range(1, 20):
        search_result = next_playlist(token, next_link)
        next_link = search_result["next"]
        print(next_link)
        for playlist in search_result["items"]:
            print(f"{count} ", end="")
            count += 1
            validated_playlist = validate_data(playlist)
            if validated_playlist:
                result.append(validated_playlist)
                print(validated_playlist)
    print(result)
    write_file(result)
    print(len(result))
    end = time.time()
    print(end - start)