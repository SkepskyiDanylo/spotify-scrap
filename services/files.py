from datetime import datetime
import json
import re
import os

#saving logs
def save_log(action: str, log_type: str, file_name: str = "logs.json") -> None:
    print(action)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs = []
    with open(file_name, "r", encoding="utf-8") as file_in:
        try:
            logs = json.load(file_in)
        except json.decoder.JSONDecodeError:
            logs.append({"timestamp": now, "type": "no_logs", "action": "file logs.json is empty, creating new one"})
        with open(file_name, "w", encoding="utf-8") as file_out:
            logs.append({"timestamp": now, "type": log_type, "action": action})
            json.dump(logs, file_out, ensure_ascii=False, indent=4)

# checking for email in description
# if emails are found returning dict{name,email,url}
def validate_data(data: dict) -> dict | None:
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    emails = re.findall(email_pattern, data["description"])
    if emails:
        save_log(action=f"Found {len(emails)} emails for {data['name']}", log_type="email_found")
        save_log(action=f"name: {data["name"]}, emails: {", ".join(emails)}, link: {data["external_urls"]["spotify"]}", log_type="playlist")
        return {
            "name": data["name"],
            "email": ", ".join(emails),
            "url": data["external_urls"]["spotify"],
        }
    save_log(action=f"Found no emails for {data['name']}", log_type="email_not_found")
    return None

# rework
def load_links(file_name: str) -> list[str]:
    with open(file_name, "r") as f:
        urls_to_upload = f.read().splitlines()
    with open("used_urls.txt", "r") as f:
        used_urls = f.read().splitlines()
    playlist_ids = []
    with open("used_urls.txt", "a") as f:
        for url in urls_to_upload:
            if url not in used_urls:
                playlist_ids.append(url[34:56])
                f.write(url + "\n")
            else:
                print(f"{url} ignored!")
    return playlist_ids

# loading used data, dict{used_links: [], used_queries: []}
def get_used_data(file_name: str = "used_data.json") -> dict[str, list] | None:
    data = {"used_links": [], "used_queries": []}
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                print(f"Json file is empty, or damaged. Will be overwritten")
    else:
        print("File not found.\nCreating new one")
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    return data

def write_file(playlist_data: list[dict]) -> None:
    with open("emails.txt", "a",  encoding='utf-8') as f:
        for playlist in playlist_data:
            f.write(f"{playlist["name"]} : {playlist['email']} : {playlist['url']}\n")