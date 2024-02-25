import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# Function to scrape data from a Wikipedia page
def scrape_wikipedia(url, decade):
    """
    Scrapes data from the given Wikipedia URL.
    
    Args:
    - url (str): The URL of the Wikipedia page to scrape.
    
    Returns:
    - list: A list containing the scraped data.
    """
    # Send a GET request to the URL
    response = requests.get(url)

    # Print the URL
    print(f"Scraping data from: {url}")

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Initialize list to store the data
    data = []

    # Find the table containing the data you want to scrape
    tables = soup.find_all("table", {"class": "wikitable"})

    # Loop through each table
    for table in tables:
        # Initialize current year
        current_year = None

        # Loop through each row in the table (skipping the header row)
        for row in table.find_all("tr"):
            # Check if the row contains a year
            year_cell = row.find("th", {"colspan": "5"})
            if year_cell:
                # Extract the year from the span class
                current_year = year_cell.text.strip()

            # Get the cells in each row
            cells = row.find_all(["td", "th"])

            # Check if there are enough cells
            if len(cells) >= 4:
                try:
                    # Extract the desired information from the cells
                    song = cells[0].text.strip()
                    artist = cells[1].text.strip()
                    peak_date = cells[2].text.strip()
                    weeks_at_number_one = cells[3].text.strip()

                    # Add the extracted data to the list with the current year
                    data.append([decade, current_year, song, artist, peak_date, weeks_at_number_one])
                except IndexError:
                    print("Error: Not enough cells in row")

    return data

# Function to process artist names
def process_artist_name(artist):
    # Split the artist name at "Featuring" if present
    parts = artist.split(" featuring ")
    # Return the first part of the split
    return parts[0]

# Function to clean the DataFrame
def clean_dataframe(df):
    """
    Cleans the DataFrame by removing unwanted characters and columns.
    
    Args:
    - df (DataFrame): The DataFrame to be cleaned.
    
    Returns:
    - DataFrame: The cleaned DataFrame.
    """
    
    # Convert 'Year' and 'Issue Date' columns to strings and concatenate them with '/' separator
    regex_pattern = r'(\d{4})'
    df['Year'] = df['Year'].str.extract(regex_pattern)
    
    df['Date'] = df['Year'].astype(str) + '/' + df['Issue Date'].astype(str)

    # Convert 'Date' column to datetime format with 'yyyy/Month day' format
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%B %d', errors='coerce')

    # Drop the 'Year' column
    columns_to_drop = ['Year','Issue Date']
    df = df.drop(columns=columns_to_drop)

    # Update 'Song of the Year' column based on 'Song' column content
    df['Song of the Year'] = df['Song'].str.contains("†", na=False)

    # Remove any text within square brackets or parentheses from 'Song' column
    df['Song'] = df['Song'].str.replace(r'\[.*?\]|\(.*?\)|\†', '', regex=True)
    df['Song'] = df['Song'].str.replace(r'\'', '', regex=True)
    df['Weeks at Number One'] = df['Weeks at Number One'].str.replace(r'\[.*?\]','',regex=True)

    # Process artist names
    df['Artist'] = df['Artist'].apply(process_artist_name)

    return df

# Initialize list to store DataFrames for each decade
dfs = []

# Iterate through decades (1980s to 2010s)
for decade in range(1980, 2030, 10):
    url = f"https://en.wikipedia.org/wiki/List_of_Billboard_Mainstream_Rock_number-one_songs_of_the_{decade}s"
    
    decade_data = scrape_wikipedia(url, decade)
    
    # Create a DataFrame for the current decade
    columns = ['Decade', 'Year', 'Issue Date', 'Song', 'Artist', 'Weeks at Number One']
    df = pd.DataFrame(decade_data, columns=columns)
    df['Song'] = df['Song'].str.replace('"', '')
    # Append the DataFrame to the list
    dfs.append(df)

# Concatenate all DataFrames into one big DataFrame
big_df = pd.concat(dfs, ignore_index=True)

# Clean the big DataFrame
big_df = clean_dataframe(big_df)

# Filter out rows with missing dates
big_df = big_df[big_df['Date'].notnull()]

# Get the directory of the current Python script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Save the big DataFrame to a CSV file in the same directory as the script
output_filename = "Rock Lists Combined.csv"
output_path = os.path.join(script_dir, output_filename)
# big_df.to_csv(output_path, index=False, encoding='utf-8')
