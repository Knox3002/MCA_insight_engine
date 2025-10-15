import streamlit as st
import pandas as pd
import os

# Load data
@st.cache_data
def load_data():
    if os.path.exists("output/enriched_dataset.csv"):
        return pd.read_csv("output/enriched_dataset.csv")
    else:
        return pd.DataFrame()

st.title("🏢 MCA Insights Engine Dashboard")

data = load_data()
if data.empty:
    st.warning("No data found. Please run the enrichment script first.")
else:
    st.success(f"Loaded {len(data)} company records.")

    # Sidebar filters
    state = st.sidebar.selectbox("Filter by State", ["All"] + sorted(data["STATE"].unique().tolist()))
    status = st.sidebar.selectbox("Filter by Status", ["All"] + sorted(data["STATUS"].unique().tolist()))

    filtered = data.copy()
    if state != "All":
        filtered = filtered[filtered["STATE"] == state]
    if status != "All":
        filtered = filtered[filtered["STATUS"] == status]

    st.dataframe(filtered)

    # Search by CIN or Name
    query = st.text_input("🔍 Search by Company Name or CIN")
    if query:
        result = data[
            data["COMPANY_NAME"].str.contains(query, case=False, na=False) |
            data["CIN"].str.contains(query, case=False, na=False)
        ]
        st.dataframe(result)

    # AI Summary
    if os.path.exists("output/daily_summary.txt"):
        st.subheader("🧠 Daily AI Summary")
        st.text(open("output/daily_summary.txt").read())

    # Simple chatbot
    st.subheader("💬 Ask about the data")
    user_q = st.text_input("Your question:")
    if user_q:
        # basic rule-based responses
        if "new" in user_q.lower() and "incorporation" in user_q.lower():
            st.write(f"Total new incorporations today: {len(data[data['STATUS']=='Active'])}")
        elif "strike" in user_q.lower() or "off" in user_q.lower():
            st.write(f"Total struck-off companies: {len(data[data['STATUS']=='Strike Off'])}")
        else:
            st.write("I'm still learning! Try asking about incorporations or status changes.")