import pandas as pd

# Function to process data
def process():

    # Read raw data and remove neutral rows
    df = pd.read_csv("data.csv", sep=',')
    df.drop(df.loc[df["Sentiment"] == 1.0].index, inplace=True)

    # Classify the data
    df['Sentiment'] = df['Sentiment'].apply(classify)

    # Write processed data to new csv file
    filename = "processed_data.csv"
    df.to_csv(filename, index=False)

# Function to classify data as 0 (negative) or 1 (positive)
def classify(x):
    if x == 0.0:
        return 0
    elif x == 2.0:
        return 1