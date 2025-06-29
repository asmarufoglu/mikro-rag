import pandas as pd

def load_data():
    url = "https://docs.google.com/spreadsheets/d/yourdataabc/export?format=csv"
    df = pd.read_csv(url)
    return df
