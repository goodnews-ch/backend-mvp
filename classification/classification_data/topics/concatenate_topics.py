import pandas as pd

DATAFRAMES = [
    ("Entertainment_News.csv", "Entertainment"),
    ("ukraine.csv", "War"),
    ("Sports_News.csv", "Sports"),
    ("Covid_and_Vaccine_News.csv", "COVID")
]

def process():
    dfs = []
    for tup in DATAFRAMES:
        dataframe, topic = tup
        # Read raw data and remove neutral rows
        df = pd.read_csv(dataframe, sep=',')

        dfs.append(df)
    
    result = pd.concat(dfs)
    result = result.drop("TITLE", 1)
    result = result.sample(frac = 1)
    result = result[~result['title'].isnull()]
    
    # Write processed data to new csv file
    filename = "cumulative_data.csv"
    result.to_csv(filename, index=False)

process()