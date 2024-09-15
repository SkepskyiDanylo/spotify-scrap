import json
import base64

from time import time
from requests import post, get


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
        response = post(url, headers=headers, data=data)
        json_data = json.loads(response.content)
        token = json_data["access_token"]

        self.end_time = time() + 3600 - 60
        self._token = token

    @property
    def token(self) -> str:
        if time() > self.end_time:
            self.refresh_token()
        return self._token


def get_auth_header(token: str) -> dict[str, str]:
    return {"Authorization": "Bearer " + token, }


def search_for_playlist(token_manager: TokenManager, search_request: str, next_link: str = None) -> dict[str, str | list] | None:
    request_link = ""

    if next_link is None:
        search_request.replace(" ", "+")
        link = "https://api.spotify.com/v1/search?q="
        queue = str(search_request) + "&limit=50&type=playlist"
        request_link = link + queue
    elif next_link:
        request_link = next_link

    headers = get_auth_header(token_manager.token)
    response = get(request_link, headers=headers)
    if response.status_code == 200:
        json_data = json.loads(response.content)
        return json_data["playlists"]
    return None

def get_playlist_data(token_manager: TokenManager, playlist_id: str) -> dict[str, str | list] | None:
    url = "https://api.spotify.com/v1/playlists/" + str(playlist_id)
    headers = get_auth_header(token_manager.token)
    response = get(url, headers=headers)
    if response.status_code == 200:
        json_data = json.loads(response.content)
        return json_data
    else:
        return None