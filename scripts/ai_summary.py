import pandas as pd
from datetime import datetime

def generate_summary():
    log_path = "output/daily_change_log.csv"
    summary_path = "output/daily_summary.txt"

    df = pd.read_csv(log_path)

    # count change types
    new_incorp = df[df['Change_Type'] == 'New Incorporation'].shape[0]
    dereg = df[df['Change_Type'] == 'Deregistered'].shape[0]
    updates = df[df['Change_Type'] == 'Field Update'].shape[0]

    # create text summary
    summary = f"""
Daily Summary Report – {datetime.now().strftime('%Y-%m-%d')}
------------------------------------------------------------
New incorporations : {new_incorp}
Deregistered       : {dereg}
Updated records    : {updates}
------------------------------------------------------------
Total changes      : {len(df)}
"""

    # save summary
    with open(summary_path, "w") as f:
        f.write(summary)

    print("✅ Daily summary generated successfully!")
    print(summary)

if __name__ == "__main__":
    generate_summary()