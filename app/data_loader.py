import pandas as pd
import os

def load_titanic_data(path=None):
    if path is None:
        # Get the directory of this file and go up one level
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        path = os.path.join(parent_dir, "titanic.csv")
    print(f"Loading from path: {path}")
    df = pd.read_csv(path)
    return df

# Example: preprocessing
def preprocess(df):
    df['Age'].fillna(df['Age'].median(), inplace=True)
    df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
    return df
