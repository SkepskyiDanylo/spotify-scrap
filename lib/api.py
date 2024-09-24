import base64
import json
import logging
import re
import httpx
from time import time


logging.basicConfig(level=logging.WARNING)


class TokenManager:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.end_time = 0
        self.client_id = client_id
        self._client_secret = client_secret
        self._token = None

    def refresh_token(self) -> None:
        auth_string = self.client_id + ":" + self._client_secret
        auth_bytes = auth_string.encode('utf-8')
        auth_b64 = str(base64.b64encode(auth_bytes), 'utf-8')
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_b64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        response = httpx.post(url, headers=headers, data=data)
        json_data = response.json()
        token = json_data["access_token"]

        self.end_time = time() + 3600 - 60
        self._token = token

    @property
    def token(self) -> str:
        if time() > self.end_time:
            self.refresh_token()
        return self._token


def validate_playlist(data: dict) -> dict | None:
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    emails = re.findall(email_pattern, data["description"])
    if emails:
        print(f"Found {len(emails)} emails for {data['name']}")
        return {
            "name": data["name"],
            "email": ", ".join(emails),
            "link": data["external_urls"]["spotify"],
        }
    print(f"Found no emails for {data['name']}")
    return None


def get_auth_header(token: str) -> dict[str, str]:
    return {"Authorization": "Bearer " + token, }


def search_for_playlist(token_manager: TokenManager,
                        search_request: str,
                        next_link: str = None) -> dict[str, str | list] | None:
    request_link = ""

    if next_link is None:
        search_request.replace(" ", "+")
        link = "https://api.spotify.com/v1/search?q="
        queue = str(search_request) + "&limit=50&type=playlist"
        request_link = link + queue
    elif next_link:
        request_link = next_link

    headers = get_auth_header(token_manager.token)
    response = httpx.get(request_link, headers=headers)
    if response.status_code == 200:
        json_data = json.loads(response.content)
        return json_data["playlists"]
    return None


def get_playlist_data(token_manager: TokenManager, playlist_id: str) -> dict[str, str | list] | None:
    url = "https://api.spotify.com/v1/playlists/" + str(playlist_id)
    headers = get_auth_header(token_manager.token)
    try:
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            json_data = response.json()
            result = validate_playlist(json_data)
            return result
        else:
            return
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        logging.warning(f"Failed to get playlist data for {playlist_id}")


def get_track_data(token_manager: TokenManager,
                         playlist_link: str, top_count: int = 5) -> list[tuple]:
    result = []
    start_link = "https://api.spotify.com/v1/playlists/" + playlist_link[34:56]

    headers = get_auth_header(token_manager.token)
    response = httpx.get(start_link, headers=headers)  # Асинхронный GET-запрос
    json_data = response.json()
    link = json_data["tracks"]["href"]
    count_of_tracks = 0
    while True:
        if not link:
            break

        headers = get_auth_header(token_manager.token)
        response = httpx.get(link, headers=headers)  # Асинхронный GET-запрос
        json_data = response.json()
        tracks = json_data["items"]
        link = json_data["next"]

        for track in tracks:
            try:
                count_of_tracks += 1
                name = track["track"]["name"]
                artist = track["track"]["artists"][0]["name"]
                popularity = track["track"]["popularity"]
                url = track["track"]["external_urls"]["spotify"]
                print(f"{name=}, {artist=}, {popularity=}, {url=}")
                result.append((name, artist, popularity, url))
            except TypeError:
                print("Error:", track)

    result.sort(key=lambda x: x[2], reverse=True)
    return result[:top_count]