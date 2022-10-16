import pandas as pd

DATAFRAMES = [
    ("Entertainment_News.csv", "Entertainment"),
    ("ukraine.csv", "War"),
    ("Sports_News.csv", "Sports"),
    ("Covid_and_Vaccine_News.csv", "COVID")
]

def process():
    for tup in DATAFRAMES:
        dataframe, topic = tup
        # Read raw data and remove neutral rows
        df = pd.read_csv(dataframe, sep=',')

        # Classify the data
        df['Topic'] = df['Topic'].apply(lambda x: topic)

        # Write processed data to new csv file
        filename = dataframe
        df.to_csv(filename, index=False)
    
process()