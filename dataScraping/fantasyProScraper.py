import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_player_names():
    # List of all active players is at this URL
    url = f'https://www.fantasypros.com/nba/stats/overall.php'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Assuming the stats are present in a table with the class 'table'
        table = soup.find('table', class_='table')

        # Extracting column headers
        headers = [th.text.strip() for th in table.find('thead').find_all('th')]

        # Extracting rows of data
        rows = []
        for row in table.find('tbody').find_all('tr'):
            row_data = [td.text.strip() for td in row.find_all('td')]
            row_data = row_data[headers.index('Player')]
            # Get rid of quotation marks & team info
            row_data = re.search(r'[^A-Za-z]*([A-Za-z\ \-\'\.]+)', row_data).group()
            # remove dots, apostrophes, "Jr" for URL stuff later
            row_data = row_data.replace('Jr.', '').replace('.', '').replace("'",'')
            # Convert to URL formatting
            row_data = row_data.replace(' ', '-')
            # Remove roman numerals
            row_data = re.sub("-I+[\ \-\r\n]*$", '', row_data)
            row_data = re.sub("-IV[\ \-\r\n]*$", '', row_data)
            # Remove trailing dashes
            row_data = re.sub('-+$', '', row_data)
            # Further convert to URL formatting
            row_data = row_data.lower()
            rows.append(row_data)

        # Creating a DataFrame
        df = pd.DataFrame(rows, columns=['Player'])

        return df
    else:
        print(f"Failed to retrieve data from {url}")
        return None

def scrape_player_stats(player_url):
    url = f'https://www.fantasypros.com{player_url}'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Assuming the stats are present in a table with the class 'table'
        table = soup.find('table', class_='table')

        # Extracting column headers
        headers = [th.text.strip() for th in table.find('thead').find_all('th')]

        # Extracting rows of data
        rows = []
        for row in table.find('tbody').find_all('tr'):
            row_data = [td.text.strip() for td in row.find_all('td')]
            rows.append(row_data)

        # Creating a DataFrame
        df = pd.DataFrame(rows, columns=headers)

        # Selecting the last 11 games
        last_11_games = df.head(11)

        return last_11_games
    else:
        print(f"Failed to retrieve data from {url}")
        return None

def save_to_csv(player_name, stats_df):
    # Save the DataFrame to a CSV file
    filename = f"./playerData/{player_name}.csv"
    stats_df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    scrape_player_names().to_csv('./../players.csv', index=False) # Save all player names
    player_url = '/nba/games/shai-gilgeous-alexander.php'

    player_stats = scrape_player_stats(player_url)
    if player_stats is not None:
        player_name = player_url.split('/')[-1]
        save_to_csv(player_name.rstrip('.php'), player_stats)

if __name__ == "__main__":
    main()
