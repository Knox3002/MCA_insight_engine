from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Load enriched dataset
data_file = "output/enriched_dataset.csv"
if os.path.exists(data_file):
    df = pd.read_csv(data_file)
else:
    df = pd.DataFrame()

@app.route('/search_company', methods=['GET'])
def search_company():
    query = request.args.get('q', '')
    state = request.args.get('state', None)
    status = request.args.get('status', None)

    if df.empty:
        return jsonify({"error": "Dataset not loaded"}), 500

    result = df.copy()
    if query:
        result = result[
            result["COMPANY_NAME"].str.contains(query, case=False, na=False) |
            result["CIN"].str.contains(query, case=False, na=False)
        ]
    if state:
        result = result[result["STATE"] == state]
    if status:
        result = result[result["STATUS"] == status]

    return jsonify(result.to_dict(orient='records'))

if __name__ == "__main__":
    app.run(port=5000, debug=True)