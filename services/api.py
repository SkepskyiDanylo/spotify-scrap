import json

from requests import post, get
import base64


def get_token(client_id: str, client_secret: str) -> str:
    auth_string = client_id + ":" + client_secret
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
    return token


def get_auth_header(token: str) -> dict[str, str]:
    return {"Authorization": "Bearer " + token, }


def get_playlist_data(token, playlist_id):
    url = "https://api.spotify.com/v1/playlists/" + str(playlist_id)
    headers = get_auth_header(token)
    response = get(url, headers=headers)
    json_data = json.loads(response.content)
    return json_data


def search_for_playlist(token: str, search_request: str, next_link: str = None) -> list[dict[str, str]]:
    search_request.replace(" ", "+")
    link = "https://api.spotify.com/v1/search?q="
    queue = str(search_request) + "&limit=50&type=playlist"
    headers = get_auth_header(token)
    response = get(link + queue, headers=headers)
    json_data = json.loads(response.content)
    return json_data["playlists"]


def next_playlist(token: str, next_link: str) -> list[dict[str, str]]:
    headers = get_auth_header(token)
    response = get(next_link, headers=headers)
    json_data = json.loads(response.content)
    return json_data["playlists"]