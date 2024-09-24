import csv
import json
import os
import openpyxl

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def get_used_data() -> dict[str, list, int] | None:
    file_name = os.path.join(BASE_DIR, "assets", "used_data.json")
    data = {"used_ids": [], "last_playlist_id": 0}
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                print("'used_data' Json file is empty, or damaged. Will be overwritten")
    else:
        print("File not found.\nCreating new one")
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    return data


def upload_used_data(data: dict) -> None:
    file_name = os.path.join(BASE_DIR, "assets", "used_data.json")
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def check_for_duplicates(playlist_link: str) -> bool:
    data = get_used_data()
    used_ids = data["used_ids"]
    playlist_id = playlist_link[34:56]
    if playlist_id not in used_ids:
        used_ids.append(playlist_id)
        data["used_ids"] = used_ids
        upload_used_data(data)
        return True
    print(f"Found duplicate for {playlist_link}")
    return False


class FileManager:
    def __init__(self) -> None:
        self.folder = Path(BASE_DIR, "files")
        self.file_name = None

    def load_links(self, file_name: str) -> list[str] | None:
        self.file_name = file_name
        if self.file_name.endswith(".txt"):
            return self.from_txt
        elif self.file_name.endswith(".csv"):
            return self.from_csv
        elif self.file_name.endswith(".xlsx"):
            return self.from_xlsx
        else:
            print(f"{self.file_name} file type not supported")
            return []

    def load_folder(self) -> list:
        playlist_ids = []
        for file_path in self.folder.iterdir():
            if file_path.is_file():
                print(f"Opening {file_path}")
                playlist_ids = playlist_ids + self.load_links(str(file_path))
        return playlist_ids

    @property
    def from_txt(self) -> list[str]:
        try:
            with open(self.file_name, "r") as f:
                urls_to_upload = f.read().splitlines()
        except FileNotFoundError:
            print("File not found")

        data = get_used_data()
        used_ids = data["used_ids"]
        playlist_ids = []
        for link in urls_to_upload:
            if (isinstance(link, str)
                    and link.startswith("https://open.spotify.com/playlist/")):
                playlist_id = link[34:56]
                if playlist_id not in used_ids:
                    playlist_ids.append(playlist_id)
                    used_ids.append(playlist_id)
                else:
                    print(f"{link} ignored!")
            else:
                print(f"{link} is not spotify url")
        data["used_ids"] = used_ids
        upload_used_data(data)
        print(f"Found {len(playlist_ids)} playlists")
        return playlist_ids

    @property
    def from_csv(self) -> list[str] | None:
        try:
            column_name = input("Enter column name with links: ")
            with open(self.file_name, newline='', encoding='utf-8') as csvfile:
                urls_data = csv.DictReader(csvfile)
                data = get_used_data()
                used_ids = data["used_ids"]
                playlist_ids = []

                for row in urls_data:
                    if column_name in row:
                        link = row[column_name.strip()]
                        if isinstance(link, str):
                            if link.startswith("https://open.spotify.com/playlist/"):
                                p_id = link[34:56]
                                if p_id in used_ids:
                                    print(f"{link} ignored!")
                                else:
                                    playlist_ids.append(p_id)
                                    used_ids.append(p_id)
                            else:
                                print(f"{link} is not spotify url")
                    data["used_ids"] = used_ids
                    upload_used_data(data)

                if playlist_ids:
                    print(f"Found {len(playlist_ids)} playlists")
                    return playlist_ids

                print(f"Found no playlists for {self.file_name} in column {column_name}\n"
                      f"Please try again")
                return []

        except FileNotFoundError:
            print("File not found")
            return []


    @property
    def from_xlsx(self) -> list[str]:
        sheet_name = input("Enter sheet name: ")
        column_number = int(input("Enter column number: "))
        try:
            workbook = openpyxl.load_workbook(self.file_name)
            sheet = workbook[sheet_name]
        except FileNotFoundError:
            print("File not found")
            return []

        data = get_used_data()
        used_ids = data["used_ids"]
        playlist_ids = []

        for row in sheet.iter_rows(min_col=column_number,
                                   max_col=column_number,
                                   values_only=True):
            link = row[0]
            if (isinstance(link, str)
                    and link.startswith("https://open.spotify.com/playlist/")):
                playlist_id = link[34:56]
                if playlist_id in used_ids:
                    print(f"{link} ignored!")
                else:
                    playlist_ids.append(playlist_id)
                    used_ids.append(playlist_id)
            else:
                print(f"{link} is not spotify url")

        data["used_ids"] = used_ids
        upload_used_data(data)

        if playlist_ids:
            print(f"Found {len(playlist_ids)} playlists")
            return playlist_ids

        print(f"Found no playlists for {self.file_name} in column {column_number}")
        return []