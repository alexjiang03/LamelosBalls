import pandas as pd

def main ():
    df = pd.read_csv ("./league_four_factors_2024-02-02.csv")

    percentage_columns = ["OFFENSE: eFG%", "OFFENSE: TOV%", "OFFENSE: ORB%", "DEFENSE: eFG%",
                          "DEFENSE: TOV%", "DEFENSE: ORB%"]

    for column in percentage_columns:
        if column in df.columns and df[column].dtype == 'object':
            df[column] = df[column].replace('%', '', regex=True)

            if df[column].str.contains('\.').any():
                df[column] = pd.to_numeric(df[column].str.rstrip('%'), errors='coerce') / 100

            else:
                df[column] = pd.to_numeric(df[column], errors='coerce') / 100

            
    df.to_csv("./league_four_factors_2024-02-02.csv", index=False)


            

if __name__ == "__main__":
    main()