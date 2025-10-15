import os
import pandas as pd

# ✅ Use paths relative to the MAIN folder
STATE_DATA_FOLDER = "state_data"
MASTER_DATA_FILE = "output/master_dataset.csv"

def integrate_state_data():
    all_data = []
    files = [f for f in os.listdir(STATE_DATA_FOLDER) if f.endswith(".csv")]

    print(f"\n🔍 Found {len(files)} state files: {files}\n")

    for file in files:
        file_path = os.path.join(STATE_DATA_FOLDER, file)
        try:
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.strip().str.upper()
            df["STATE"] = os.path.splitext(file)[0]
            all_data.append(df)
            print(f"✅ Processed {file} ({len(df)} records)")
        except Exception as e:
            print(f"❌ Error reading {file}: {e}")

    if not all_data:
        print("⚠ No CSV files found. Check your 'state_data' folder path.")
        return

    master_df = pd.concat(all_data, ignore_index=True)
    master_df.drop_duplicates(subset=["CIN"], inplace=True)
    master_df.fillna("", inplace=True)
    master_df.to_csv(MASTER_DATA_FILE, index=False)

    print(f"\n✅ Master dataset created successfully: {MASTER_DATA_FILE}")
    print(f"📊 Total records: {len(master_df)}\n")

if __name__ == "__main__":
    integrate_state_data()