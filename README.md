# MCA Insight Engine

**MCA (Ministry of Corporate Affairs) Insight Engine** is a Python project to track changes in Ministry of Corporate Affairs (MCA) company data over time, enrich those changes with additional information, and provide a web interface + AI-powered insights.

---

## 🚀 Features

- Ingest and unify MCA datasets from different states  
- Detect day-to-day changes:
  - New incorporations  
  - Removed / struck off companies  
  - Updated fields (e.g. status, capital, address)  
- Enrich detected changes with further data (e.g. director names, industry) via external sources  
- Web dashboard (Flask / Streamlit) to:
  - Search by CIN or company name  
  - Filter by state, year, status  
  - View visualizations (change trends)  
  - Show enriched details  
- Generate daily summary reports  
- Simple chatbot or query interface to ask about changes

---

## 📂 Repository Structure

```text
MCA_insight_engine/
├── app.py                 # Entry point for the dashboard / web app  
├── README.md              # This file  
├── scripts/               # Scripts for data processing & update logic  
│   ├── ingest.py  
│   ├── diff.py  
│   ├── enrich.py  
│   └── summarize.py  
├── state_data/             # Raw / intermediate state-wise MCA data  
├── output/                 # Output files: master dataset, change logs, summaries  
└── requirements.txt        # Python dependencies  

🛠 Installation & Setup

Clone the repository

git clone https://github.com/Knox3002/MCA_insight_engine.git
cd MCA_insight_engine


Create a virtual environment (optional but recommended)

python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate


Install dependencies

pip install -r requirements.txt


Prepare data

Put state-wise MCA CSVs into state_data/

Adjust any configuration (e.g. paths) in scripts if needed

Run ingestion / diff / enrichment scripts

python scripts/ingest.py
python scripts/diff.py
python scripts/enrich.py
python scripts/summarize.py


Start the web app

python app.py


Then open http://localhost:5000 (or whichever port) in your browser.

✅ Usage Examples

Search for a company by CIN or name in the UI

Filter changes by state or year

View the summary dashboard showing new vs removed vs updated counts

Ask a chatbot (if implemented) like:

“Show me the new incorporations in Maharashtra in the last month”

🧩 How it works (high-level flow)

Ingest / Clean — Load state CSVs, standardize columns, merge

Diffing — Compare new vs previous snapshot → detect changes

Enrichment — For changed companies, fetch extra data from APIs / web sources

Summarization — Compute daily summary stats

Web + Chat Interface — Frontend + backend to query, visualize, interact

⚠️ Limitations / Assumptions

The data sources (MCA CSVs) must follow a consistent schema

Enrichment depends on external APIs / scraping — may face rate limits or missing data

The “daily snapshot” simulation assumes you maintain past copies

The chatbot is basic (rule-based or uses a lightweight LLM), not enterprise-grade

📦 Dependencies

See requirements.txt for full list. Key packages may include:

pandas, numpy — for data processing

requests, beautifulsoup4 — for web scraping / API calls

Flask or Streamlit — for UI

(Optional) openai or langchain — if using LLMs for chat insights

📄 License & Credits

Specify your license (e.g. MIT, Apache 2.0) here.
You can also acknowledge data sources (MCA / government CSV portals) and any APIs you use.

🚧 Next Steps (Possible Enhancements)

Add authentication / user login

Cache enriched data / use incremental enrichment

Improve chatbot with context / memory

Deploy on a cloud / containerize

Add alerting (email/SMS) for big changes
