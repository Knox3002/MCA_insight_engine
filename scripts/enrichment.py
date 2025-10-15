import pandas as pd
import os
import ast
import time
from typing import Dict, Any

# Paths (relative to main project folder)
CHANGE_LOG_FILE = "output/daily_change_log.csv"
ENRICHED_FILE = "output/enriched_dataset.csv"

# How many changed companies to enrich (50-100 per task spec)
sample_size = 50

# Timeout between requests if you implement real web calls (seconds)
REQUEST_PAUSE = 0.5
from requests_module import real_enrich_single  # your real enrichment function here

def parse_new_value(val: Any) -> Dict[str, Any]:
    """
    The change log may store New_Value as a dict, or as a string repr of a dict.
    This function returns a dictionary safely.
    """
    if isinstance(val, dict):
        return val
    if pd.isna(val) or val == "":
        return {}
    # Try literal eval
    try:
        parsed = ast.literal_eval(val)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass
    # Fallback: return empty dict
    return {}


def dummy_enrich_single(cin: str, base_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dummy enrichment function:
    - Returns a dict containing sector, directors, company_type, and a fake source URL.
    Replace or extend this with real API/scraping calls.
    """
    # Example heuristic: map NIC_CODE-like to a broad sector (very naive)
    nic = base_info.get("NIC_CODE") or base_info.get("NIC", "") or ""
    try:
        nic_int = int(str(nic)[:2]) if nic else None
    except Exception:
        nic_int = None

    if nic_int is None:
        sector = "Unknown"
    elif nic_int < 10:
        sector = "Agriculture"
    elif nic_int < 40:
        sector = "Manufacturing"
    elif nic_int < 70:
        sector = "Services"
    else:
        sector = "Other"

    # Fake director list generator
    directors = [
        f"Director {cin[-3:]}A",
        f"Director {cin[-3:]}B"
    ]

    # Fake company type mapping
    company_type = base_info.get("COMPANY_CLASS") or base_info.get("COMPANY_TYPE") or "Private Limited"

    return {
        "SECTOR": sector,
        "DIRECTORS": "; ".join(directors),
        "COMPANY_TYPE": company_type,
        "REGISTERED_OFFICE": base_info.get("REGISTERED_OFFICE_ADDRESS", ""),
        "SOURCE_URL": f"https://www.zaubacorp.com/company-search/U12345MH2020PTC000001{cin}"
    }


def enrich_changes(sample_df: pd.DataFrame) -> pd.DataFrame:
    """
    For each row in sample_df, perform enrichment (currently dummy).
    Returns a dataframe ready to save.
    """
    enriched_rows = []
    total = len(sample_df)
    for idx, row in sample_df.iterrows():
        cin = row.get("CIN", "")
        new_val = parse_new_value(row.get("NEW_VALUE", ""))

        # Gather some base info for enrichment context
        base_info = {}
        # new_val could be the company dict or just company name string — handle both
        if isinstance(new_val, dict):
            base_info = {k.upper(): v for k, v in new_val.items()}
        else:
            # If NEW_VALUE is not dict, try to use COMPANY_NAME column in change log if present
            base_info["COMPANY_NAME"] = row.get("NEW_VALUE") or ""
        # Try to populate NIC_CODE / STATE from other change_log columns if present
        if "STATE" not in base_info and "STATE" in row:
            base_info["STATE"] = row["STATE"]

        enriched = real_enrich_single(cin, base_info)
        # -------------------------------------------------------------------

        enriched_row = {
            "CIN": cin,
            "COMPANY_NAME": base_info.get("COMPANY_NAME", "") or enriched.get("COMPANY_NAME", ""),
            "STATE": base_info.get("STATE", "") or row.get("STATE", ""),
            "STATUS": row.get("CHANGE_TYPE", ""),
            "SECTOR": enriched.get("SECTOR", ""),
            "DIRECTORS": enriched.get("DIRECTORS", ""),
            "COMPANY_TYPE": enriched.get("COMPANY_TYPE", ""),
            "REGISTERED_OFFICE": enriched.get("REGISTERED_OFFICE", ""),
            "SOURCE": "ZaubaCorp",
            "FIELD": row.get("FIELD_CHANGED", ""),
            "SOURCE_URL": enriched.get("SOURCE_URL", "https://www.zaubacorp.com/company-search/U12345MH2020PTC000001" + cin)
        }
        enriched_rows.append(enriched_row)

        # polite pause if using real web calls
        time.sleep(REQUEST_PAUSE)

    return pd.DataFrame(enriched_rows)


def main():
    # Step A: check input
    if not os.path.exists(CHANGE_LOG_FILE):
        print(f"❌ Change log not found: {CHANGE_LOG_FILE}")
        print("Run step 3 (change_detection.py) first to produce daily_change_log.csv")
        return

    df = pd.read_csv(CHANGE_LOG_FILE)
    if df.empty:
        print("ℹ Change log is empty. Nothing to enrich.")
        return

    # Step B: sample up to sample_size records (we prefer recent changes at top)
    sample_count = min(sample_size, len(df))
    sample_df = df.head(sample_count).copy()  # head() keeps latest if you appended logs in order

    print(f"🔍 Enriching {sample_count} companies (sample from change log) ...")

    enriched_df = enrich_changes(sample_df)

    # Re-order columns to the requested final format
    final_cols = [
        "CIN", "COMPANY_NAME", "STATE", "STATUS", "SECTOR",
        "DIRECTORS", "COMPANY_TYPE", "REGISTERED_OFFICE",
        "SOURCE", "FIELD", "SOURCE_URL"
    ]
    # ensure all columns present
    for c in final_cols:
        if c not in enriched_df.columns:
            enriched_df[c] = ""

    enriched_df = enriched_df[final_cols]

    enriched_df.to_csv(ENRICHED_FILE, index=False)
    print(f"✅ Enrichment complete. Saved to {ENRICHED_FILE}")
    print(f"📊 Enriched records: {len(enriched_df)}")


if __name__ == "__main__":
    main()