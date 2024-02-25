Wikipedia Scraper for Billboard Mainstream Rock Number One Songs
----
This Python script scrapes data from Wikipedia pages listing Billboard Mainstream Rock number one songs for each decade, cleans the data, and saves it to a CSV file.

Prerequisites
---
    Python 3.x
    BeautifulSoup4
    Pandas
    spotipy
    WebScrape (this is optional, as I used it to webscrape billboard 100)

Installation
----
    Clone this repository to your local machine:
        git clone https://github.com/WanHayl/Spotify-Connector.git

        Install the required Python packages:
        pip install beautifulsoup4 pandas spotipy

Usage
---
Open a terminal or command prompt.

Navigate to the directory containing the script.

Run the script: python wikipedia_scraper.py
The script will scrape data from Wikipedia, clean it, and save it to a CSV file named "Rock Lists Combined.csv" in the same directory.

Client Credentials: Replace 'Your-Client-ID', 'Your-Client-Secret', and 'Your-Redirect-URI' with your Spotify application's client ID, client secret, and redirect URI obtained from the Spotify Developer Dashboard.

Notes
---
    Ensure your Spotify application is registered and authorized in the Spotify Developer Dashboard.
    Handle rate limits and potential errors gracefully to avoid disruptions in API access.

Documentation
---
WEBSCRAPE PART:

    scrape_wikipedia(url, decade):
        This function takes a URL and a decade as input and scrapes data from a Wikipedia page.
        It sends a GET request to the URL, parses the HTML content, and extracts information from the tables.
        The scraped data is stored in a list of lists, where each inner list represents a row of data.

    Parameters:
        url: The URL of the Wikipedia page to scrape.
        decade: The decade for which data is being scraped.

    Returns:
        data: A list of lists containing the scraped data.

    clean_dataframe(df):
        This function cleans the DataFrame by performing the following operations:
            Concatenates the 'Year' and 'Issue Date' columns into a single 'Issue Date' column in the format 'yyyy/mm/dd'.
            Converts the 'Issue Date' column to datetime format.
            Removes the 'Year' column.
            Updates the 'Song of the Year' column based on the presence of a specific symbol in the 'Song' column.
            Removes any text within square brackets, parentheses, or a specific symbol from the 'Song' column.

    Parameters:
        df: The DataFrame to be cleaned.

    Returns:
        df: The cleaned DataFrame.

    dfs:
        A list to store DataFrames for each decade.

    big_df:
        A DataFrame that stores all scraped and cleaned data from multiple decades.

SPOTIFY PART:
        Authentication:
        The retrieve_auth function authenticates the application using the provided client credentials.

    Search for Songs:
        The search_song function searches for each song in the Spotify database based on its name and artist. It retrieves basic information about the song, such as its name, artist, album, track ID, popularity, and preview URL.

    Retrieve Audio Features:
        The get_audio_features function retrieves audio features for a list of track IDs. It handles batch processing to avoid rate limiting issues by splitting the list into batches of 100 track IDs.

    Data Processing:
        Retrieved song information and audio features are combined into a pandas DataFrame. Unnecessary columns (such as 'id', 'analysis_url', 'uri', and 'track_href') are dropped, and duplicate rows are removed.

    Output:
        The resulting DataFrame is saved to a CSV file named "Song Information.csv" in the same directory as the script.



License
---
This project is licensed under the MIT License - see the LICENSE file for details.