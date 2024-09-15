import json
import re
import os


# checking for email in description
# if emails are found returning dict{name,email,url}
def validate_data(data: dict) -> dict | None:
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


# loading used data, dict{used_links: [], used_queries: []}
def get_used_data() -> list | None:
    file_name = "used_data.json"
    data = []
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                print(f"Looking for duplicates"
                      f"'used_data' Json file is empty, or damaged. Will be overwritten")
    else:
        print("File not found.\nCreating new one")
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    return data

def upload_used_data(data: list) -> None:
    file_name = "used_data.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def unique_ids(playlist_link: str) -> bool:
    used_ids = get_used_data()
    playlist_id = playlist_link[34:56]
    if playlist_id not in used_ids:
        used_ids.append(playlist_id)
        upload_used_data(used_ids)
        return True
    print(f"Found duplicate for {playlist_link}")
    return False


def from_txt(file_name: str) -> list[str]:
    try:
        with open(file_name, "r") as f:
            urls_to_upload = f.read().splitlines()
    except FileNotFoundError:
        print("File not found")
        return []
    used_ids = get_used_data()
    playlist_ids = []
    for url in urls_to_upload:
        if url.startswith("https://open.spotify.com/playlist/"):
            playlist_id = url[34:56]
            if playlist_id not in used_ids:
                playlist_ids.append(playlist_id)
                used_ids.append(playlist_id)
            else:
                print(f"{url} ignored!")
        else:
            print(f"{url} is not spotify url")
    upload_used_data(used_ids)
    return playlist_ids


def load_links(file_name: str) -> list[str]:
    if file_name.endswith(".txt"):
        result = from_txt(file_name)
        return result
    else:
        print("File type not supported")
        return []

# def save_log(action: str, log_type: str, file_name: str = "logs.json") -> None:
#     print(action)
#     now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     logs = []
#     with open(file_name, "r", encoding="utf-8") as file_in:
#         try:
#             logs = json.load(file_in)
#         except json.decoder.JSONDecodeError:
#             logs.append({"timestamp": now, "type": "no_logs", "action": "file logs.json is empty, creating new one"})
#         with open(file_name, "w", encoding="utf-8") as file_out:
#             logs.append({"timestamp": now, "type": log_type, "action": action})
#             json.dump(logs, file_out, ensure_ascii=False, indent=4)