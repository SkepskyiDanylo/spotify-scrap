import json
import re
import os
import csv
import time
import openpyxl

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
    for link in urls_to_upload:
        if isinstance(link, str) and link.startswith("https://open.spotify.com/playlist/"):
            playlist_id = link[34:56]
            if playlist_id not in used_ids:
                playlist_ids.append(playlist_id)
                used_ids.append(playlist_id)
            else:
                print(f"{link} ignored!")
        else:
            print(f"{link} is not spotify url")
    upload_used_data(used_ids)
    return playlist_ids


def from_csv(file_name: str) -> list[str] | None:
    column_name = input("Enter column name with links: ")
    #loading used data for json file
    used_ids = get_used_data()

    try:
        with open(file_name, newline='', encoding='utf-8') as csvfile:
            data = csv.DictReader(csvfile)
            playlist_ids = []

            for row in data:
                if column_name in row:
                    link = row[column_name.strip()]
                    if isinstance(link, str) and link.startswith("https://open.spotify.com/playlist/"):
                        p_id = link[34:56]
                        if p_id in used_ids:
                            print(f"{link} ignored!")
                        else:
                            playlist_ids.append(p_id)
                            used_ids.append(p_id)
                    else:
                        print(f"{link} is not spotify url")

            #saving used ids to json file
            upload_used_data(used_ids)

            if playlist_ids:
                print(f"Found {len(playlist_ids)} playlists")
                return playlist_ids

            print(f"Found no playlists for {file_name} in column {column_name}\n"
                  f"Please try again")
            time.sleep(5)
            return

    except FileNotFoundError:
        print("File not found")
        return


def from_xslx(file_name: str) -> list[str] | None:
    sheet_name = input("Enter sheet name: ")
    column_number = int(input("Enter column number: "))
    used_ids = get_used_data()
    playlist_ids = []
    try:
        workbook = openpyxl.load_workbook(file_name)
        sheet = workbook[sheet_name]
    except FileNotFoundError:
        print("File not found")
        return

    for row in sheet.iter_rows(min_col=column_number, max_col=column_number, values_only=True):
        link = row[0]
        if isinstance(link, str) and link.startswith("https://open.spotify.com/playlist/"):
            playlist_id = link[34:56]
            if playlist_id in used_ids:
                print(f"{link} ignored!")
            else:
                playlist_ids.append(playlist_id)
                used_ids.append(playlist_id)
        else:
            print(f"{link} is not spotify url")

    upload_used_data(used_ids)

    if playlist_ids:
        print(f"Found {len(playlist_ids)} playlists")
        return playlist_ids

    print(f"Found no playlists for {file_name} in column {column_number}")
    return


def load_links(file_name: str) -> list[str] | None:
    if file_name.endswith(".txt"):
        result = from_txt(file_name)
    elif file_name.endswith(".csv"):
        result = from_csv(file_name)
    elif file_name.endswith(".xlsx"):
        result = from_xslx(file_name)
    else:
        print("File type not supported")
        result = None
    # return result




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