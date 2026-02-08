import pandas as pd
import os

# Path to raw data folder
RAW_DATA_PATH = "data/raw/"

def load_all_csvs(folder_path):
    all_files = os.listdir(folder_path)
    csv_files = [file for file in all_files if file.endswith(".csv")]

    df_list = []

    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        df["source_file"] = file  # track where data came from
        df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df

if __name__ == "__main__":
    df = load_all_csvs(RAW_DATA_PATH)
    print("Data loaded successfully!")
    print("Shape:", df.shape)
    print(df.head())
