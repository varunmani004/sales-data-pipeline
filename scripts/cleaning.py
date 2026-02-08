import pandas as pd
import os

RAW_DATA_PATH = "data/raw/"
PROCESSED_DATA_PATH = "data/processed/cleaned_sales_data.csv"

def load_raw_data(folder_path):
    all_files = os.listdir(folder_path)
    csv_files = [f for f in all_files if f.endswith(".csv")]

    df_list = []
    for file in csv_files:
        df = pd.read_csv(os.path.join(folder_path, file))
        df_list.append(df)

    return pd.concat(df_list, ignore_index=True)

def clean_data(df):
    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Convert order_date to datetime
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    # Remove rows with missing order_id
    if "order_id" in df.columns:
        df = df.dropna(subset=["order_id"])

    # Fill missing values
    df = df.fillna({
        "sales": 0,
        "quantity": 0,
        "discount": 0,
        "profit": 0
    })

    # Create derived feature
    if "sales" in df.columns and "quantity" in df.columns:
        df["total_sales"] = df["sales"] * df["quantity"]

    return df

def save_processed_data(df, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    df_raw = load_raw_data(RAW_DATA_PATH)
    df_cleaned = clean_data(df_raw)
    save_processed_data(df_cleaned, PROCESSED_DATA_PATH)

    print("Data cleaned and saved successfully!")
    print("Final shape:", df_cleaned.shape)
    print(df_cleaned.head())

