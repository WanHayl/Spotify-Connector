import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Read the CSV file and clean the band names
rock_list = r'c:\Users\dreik\Desktop\Combined_Rock_List.csv'
df = pd.read_csv(rock_list, encoding='latin1')
df['Artist'] = df['Artist'].str.replace(' ', '-')

# Initialize an empty DataFrame to store the scraped data
result_df = pd.DataFrame(columns=['Song Name', 'Artist Name', 'Debut Date', 'Peak Pos', 'Peak Weeks', 'Peak Date'])

# Iterate through each band
for band in df['Artist'].unique():
    print(f"Scraping data for {band}...")
    # Construct the URL for the band
    url = f'https://www.billboard.com/artist/{band}/chart-history/rtt/'

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    data = []

    # Find all divs with class "o-chart-results-list-row"
    rows = soup.find_all('div', class_='o-chart-results-list-row')

    # Iterate over each row
    for row in rows:
        # Find the h3 tag containing the song name
        song_name = row.find('h3', class_='artist-chart-row-title').get_text(strip=True)

        # Find all span elements within the row
        spans = row.find_all('span', class_='c-label')

        # Extract the associated data
        artist_name = spans[0].get_text(strip=True)
        debut_date = spans[1].get_text(strip=True)
        peak_pos = spans[2].get_text(strip=True)
        peak_weeks = spans[3].get_text(strip=True)
        peak_date = spans[4].get_text(strip=True)

        # Append the data to the list
        data.append([song_name, artist_name, debut_date, peak_pos, peak_weeks, peak_date])

    # Create a DataFrame from the data
    band_df = pd.DataFrame(data, columns=['Song Name', 'Artist Name', 'Debut Date', 'Peak Pos', 'Peak Weeks', 'Peak Date'])

    # Append the DataFrame for this band to the result DataFrame
    result_df = pd.concat([result_df, band_df], ignore_index=True)

# Print the final result DataFrame
print(result_df)

# Get the directory of the current Python script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Save the big DataFrame to a CSV file in the same directory as the script
output_filename = "Webscraped Bands.csv"
output_path = os.path.join(script_dir, output_filename)
result_df.to_csv(output_path, index=False, encoding='utf-8')