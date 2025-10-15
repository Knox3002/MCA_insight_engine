import requests

def real_enrich_single(cin: str, base_info: dict):
    try:
        url = f"https://api.example.com/company/{cin}"  # replace with real URL
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return {
                "SECTOR": data.get("sector", ""),
                "DIRECTORS": "; ".join(data.get("directors", [])),
                "COMPANY_TYPE": data.get("companyType", ""),
                "REGISTERED_OFFICE": data.get("registeredOffice", ""),
                "SOURCE_URL": url,
                "SOURCE": "ExampleAPI"
            }
    except Exception as e:
        print(f"Error fetching {cin}: {e}")

    # Fallback if API fails
    return {
        "SECTOR": "Unknown",
        "DIRECTORS": "",
        "COMPANY_TYPE": "",
        "REGISTERED_OFFICE": "",
        "SOURCE_URL": "",
        "SOURCE": "Fallback"
    }