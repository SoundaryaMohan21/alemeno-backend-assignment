import pandas as pd


def read_csv(file_path: str):
    df = pd.read_csv(file_path)

    # Convert date column (DD-MM-YYYY → datetime)
    df["date"] = pd.to_datetime(
        df["date"],
        format="%d-%m-%Y"
    )

    return df


def get_row_count(df):
    return len(df)