# Spotify Scraper

Spotify Scraper is a script designed to search for playlists on Spotify that contain an email address in their description.

## Overview

The script operates in two (or three) modes:

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

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/spotify-scraper.git
    ```
2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Example Usage

1. To search playlists from a file:
    ```bash
    python main.py
    ```

## License

This project is licensed under the MIT License.
