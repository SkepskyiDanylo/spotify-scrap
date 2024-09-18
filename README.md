### Spotify Scraper

Spotify Scraper is a script designed to search for playlists on Spotify that contain an email address in their description.

## Overview

The script operates in two (three) modes:

1. **Search playlists from a file**:  
   Press `1` and provide the file name, including the file extension. Supported formats are `.txt`, `.csv`, and `.xlsx`.
   
2. **Search by keyword**:  
   Press `2` and enter a search query. The script will search for up to 1,000 playlists based on the query and check their descriptions for email addresses.

## Usage

1. Download or clone the repository.
2. Ensure all required dependencies are installed.
3. Run the script and follow the console prompts.

## Requirements

- Python 3.x
- Libraries: (list required libraries)
- .env file

## Installation

1. Fork the repository
   - Press "Fork" button on right top
2. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/spotify-scraper.git
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Create app
   - Loggin or Register on [spotify develop](https://developer.spotify.com/)
   - Crete new app
5. Create .env
  ```bash
   echo CLIENT_ID='your client id'
   echo CLIENT_SECRET='your client secret'
   ```


## Example Usage

   - Execute main.py:
    ```bash
    python main.py
    ```
   - Starting message:
   ```python
   """
   This is a Spotify API service.
   It works in 2 modes:
   1. Loading playlist links from file, and check for email in their description
   2. Looking for playlists by search q (1000 playlists per q)
   3. Manually check every playlist for top 5 tracks
   Enter 1 or 2, to start working in selected mode
   If You want to exit type 'q' or 'exit' or 'stop'
   """
   ```
   - To shut program down, enter 'q' and press enter
   ## Search for playlist in file:
   - To enter search link mode enter '1' and press enter
     ```python
     "Welcome in load links mode"
     "Enter file name"
     "File should be in same directory"
     "File should be in [txt, csv, xlsx] format"
     "If you leave it empty will be used default value('links.txt')'"
     "If you want to go back to main menu, type 'q'"
     ```
   - To return to main menu enter 'q'
   - You have to enter file name including format, availible formats = .txt, .csv, .xlsx
      - For .csv file you have to enter column name
      - For xlsx file you have to enter sheet name and column number
   - If you enter wrong format, you'll get:
     ```python
     "File type not supported"
     ```
   - If you did everything right, you'll get message for each checked playlist:
     - if email not found:
     ```python
     "Found no emails for 'playlist name'"
     ```
     - if email found:
     ```python
     "Found 'count' emails for 'playlist name'"
     "name: 'playlist name', email: 'playlist emails', link: 'playlist link"
     ```
      - if link already used:
     ```python
     "'link' ignored!"
     ```
      - if link is not spotify link:
     ```python
     "'link' is not spotify url"
   - After you'll get message:
     ```python
     "Found 'count of playlist' links out of 'total playlist count'"
     "Press enter to continue"
   - Press enter, and enter type of songs, tracks will be added into spotify_emails.sqlite database
     ```python
     "Uploading to db
     "Enter the type of songs: "
     ```
     ```bash
     | id  | name          | email       | link            | type            |
     |-----|---------------|-------------|-----------------|-----------------|
     | 1   | playlist name | email       | playlist link   | type you entered|
     ```
   - You`re done, you'll be transfered to start message of load links mode

     ## Search for playlist in file:
     - Enter '2' and press enter
     python
     "Welcome in search mode"
     "Enter your search query or 'q' to go back to main menu"
     "Search q: "
     
     - To return to main menu enter 'q'
     - You have to enter search q
     - Once you did it, script will automatically search for playlists(up to 1000)
     - You'll get same messages as in load links mode
