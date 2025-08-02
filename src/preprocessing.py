import pandas as pd
import os

RAW_DATA_PATH = "data/raw/rentfaster.csv"
PROCESSED_DATA_PATH = "data/processed/cleaned_rentals.csv"

def load_data(path=RAW_DATA_PATH):
    """Load raw rental listings dataset."""
    df = pd.read_csv(path)
    print(f"Loaded dataset with {len(df)} rows and {len(df.columns)} columns.")
    return df

def preprocess_data(df):
    """Clean and preprocess the dataset."""
    # keep only Vancouver rentals and create a copy to avoid chained warnings
    df = df[df['city'].str.lower() == 'vancouver'].copy()

    # clean beds column: replace "Studio" with 1 and extract numeric values
    df['beds'] = df['beds'].astype(str)
    df['beds'] = df['beds'].replace({'Studio': '1'})
    df['beds'] = df['beds'].str.extract(r'(\d+)')
    df['beds'] = pd.to_numeric(df['beds'], errors='coerce')

    # clean sq_feet column: extract numeric values only
    if 'sq_feet' in df.columns:
        df['sq_feet'] = df['sq_feet'].astype(str).str.extract(r'(\d+)')
        df['sq_feet'] = pd.to_numeric(df['sq_feet'], errors='coerce')

    # convert numeric columns
    for col in ['price', 'baths']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # fill missing sq_feet with median if the column exists
    if 'sq_feet' in df.columns and df['sq_feet'].isnull().sum() > 0:
        df['sq_feet'] = df['sq_feet'].fillna(df['sq_feet'].median())

    # drop rows with missing critical values
    cols_to_check = ['price', 'beds', 'baths']
    if 'sq_feet' in df.columns:
        cols_to_check.append('sq_feet')
    df = df.dropna(subset=cols_to_check)

    # identify categorical columns to encode (excluding city, province, address, link)
    categorical_cols = [col for col in df.select_dtypes(include='object').columns
                        if col not in ['city', 'province', 'address', 'link']]

    # one-hot encode categorical columns
    if categorical_cols:
        df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # quick stats for sanity check
    print("Preprocessing complete.")
    print(f"Cleaned dataset has {len(df)} rows.")
    print(f"Price range: {df['price'].min()} - {df['price'].max()}")
    print(f"Average price: {df['price'].mean():.2f}")
    print(f"Beds range: {df['beds'].min()} - {df['beds'].max()}")
    return df

def save_data(df, path=PROCESSED_DATA_PATH):
    """Save cleaned dataset to CSV."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved cleaned dataset to {path}")

if __name__ == "__main__":
    data = load_data()
    clean_data = preprocess_data(data)
    save_data(clean_data)
