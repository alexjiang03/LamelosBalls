import pandas as pd
import os

team_data_file = "./teamData/league_four_factors_2024-02-02.csv"

nba_cities = ["Atlanta", "Boston", "Brooklyn", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", 
              "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", 
              "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", 
              "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"]

nba_city_abbreviations = ["ATL", "BOS", "BKN", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", "LAC", 
                          "LAL", "MEM", "MIA", "MIL", "MIN", "NOR", "NYK", "OKC", "ORL", "PHI", "PHO", "POR", "SAC", 
                          "SAS", "TOR", "UTH", "WAS"]

def name_to_abbrev (fullname):
    index = nba_cities.index(fullname)
    return nba_city_abbreviations[index]

def insert_col (file, col_name):
    dataframe = pd.read_csv (file)
    dataframe [col_name] = ""
    dataframe.to_csv (file, index=False)

def remove_col (file, col_name):
    dataframe = pd.read_csv (file)
    dataframe = dataframe.drop (columns=col_name)
    dataframe.to_csv (file, index=False)

def insert_opp_data (player_data_file):

    df1 = pd.read_csv (team_data_file)
    df2 = pd.read_csv (player_data_file)

    if "OPP" in df2.columns:
        df2 = pd.merge(df2, df1, how='left', left_on='OPP', right_on='OPP', suffixes=('', '_2'))
        df2 = df2.drop(columns=["OPP"])
        df2.to_csv (player_data_file, index=False)



def main ():
    remove_columns = ["Diff Rank", "OFFENSE: Pts/Poss Rank", "OFFENSE: eFG% Rank", "OFFENSE: TOV% Rank", 
                      "OFFENSE: ORB% Rank", "OFFENSE: FT Rate Rank", "DEFENSE: Pts/Poss Rank", "DEFENSE: eFG% Rank",
                      "DEFENSE: TOV% Rank", "DEFENSE: ORB% Rank", "DEFENSE: FT Rate Rank"]

    remove_col (team_data_file, remove_columns)

    df = pd.read_csv (team_data_file)

    if "Team" in df.columns:
        df = df.rename (columns={"Team": "OPP"})
        df.to_csv (team_data_file, index=False)

    if "OPP" not in df.columns:
        print("Column 'OPP' not found in the CSV file.")
        return

    df = df[df["OPP"] != "Average"]
    df["OPP"] = df["OPP"].apply(name_to_abbrev)

    df.to_csv(team_data_file, index=False)

    player_data_directory = "./playerData/"
    if not os.path.exists (player_data_directory):
            print (f"Directory '{player_data_directory}' not found.")
            return
    
    for player_file in os.listdir(player_data_directory):
        file_path = os.path.join (player_data_directory, player_file)
        print (file_path)
        if os.path.isfile (file_path):
            insert_opp_data(file_path)

if __name__ == "__main__":
    main()