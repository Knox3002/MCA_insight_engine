import pandas as pd
import os
from datetime import datetime

# ✅ Paths relative to the main folder
OLD_DATA_FILE = "data_snapshot/day1_master_dataset.csv"
NEW_DATA_FILE = "data_snapshot/day2_master_dataset.csv"
CHANGE_LOG_FILE = "output/daily_change_log.csv"

def detect_changes():
    if not (os.path.exists(OLD_DATA_FILE) and os.path.exists(NEW_DATA_FILE)):
        print("⚠ Missing one of the snapshot files (day1 or day2).")
        return

    old_df = pd.read_csv(OLD_DATA_FILE)
    new_df = pd.read_csv(NEW_DATA_FILE)

    old_df.columns = old_df.columns.str.upper().str.strip()
    new_df.columns = new_df.columns.str.upper().str.strip()

    changes = []
    today = datetime.now().strftime("%Y-%m-%d")

    # 🔹 New incorporations
    new_cins = set(new_df["CIN"]) - set(old_df["CIN"])
    for cin in new_cins:
        company = new_df[new_df["CIN"] == cin].iloc[0]
        changes.append({
            "CIN": cin,
            "CHANGE_TYPE": "New Incorporation",
            "FIELD_CHANGED": "",
            "OLD_VALUE": "",
            "NEW_VALUE": company["COMPANY_NAME"],
            "DATE": today
        })

    # 🔹 Deregistrations
    removed_cins = set(old_df["CIN"]) - set(new_df["CIN"])
    for cin in removed_cins:
        company = old_df[old_df["CIN"] == cin].iloc[0]
        changes.append({
            "CIN": cin,
            "CHANGE_TYPE": "Deregistered",
            "FIELD_CHANGED": "",
            "OLD_VALUE": company["COMPANY_NAME"],
            "NEW_VALUE": "",
            "DATE": today
        })

    # 🔹 Field-level updates
    common_cins = set(old_df["CIN"]).intersection(new_df["CIN"])
    for cin in common_cins:
        old_row = old_df[old_df["CIN"] == cin].iloc[0]
        new_row = new_df[new_df["CIN"] == cin].iloc[0]

        for col in ["STATUS", "AUTHORIZED_CAPITAL", "PAID_UP_CAPITAL"]:
            if str(old_row[col]) != str(new_row[col]):
                changes.append({
                    "CIN": cin,
                    "CHANGE_TYPE": "Field Update",
                    "FIELD_CHANGED": col,
                    "OLD_VALUE": old_row[col],
                    "NEW_VALUE": new_row[col],
                    "DATE": today
                })

    # 🔹 Save change log
    if changes:
        change_df = pd.DataFrame(changes)
        change_df.to_csv(CHANGE_LOG_FILE, index=False)
        print(f"\n✅ Change detection complete! Saved to {CHANGE_LOG_FILE}")
        print(f"📊 Total changes found: {len(change_df)}")
    else:
        print("\nℹ No changes detected between snapshots.")

if __name__ == "__main__":
    detect_changes()