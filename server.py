import re
import os
import io
import json
import logging
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file, render_template
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.messages import HumanMessage

app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

# Template headers can be read from csv later
TEMPLATE_HEADERS = [
    "Delete", "Contract Number", "Contract Description", "Contract Type",
    "Company Id", "Purchaser Id", "Marketer Id", "Marketer Isq",
    "Start Date", "End Date", "Contract Xref1", "Contract Xref2",
    "Dated Effective From Date", "Dated Effective To Date",
    "Measurement Point Id", "MP Effective From Date",
    "MP Effective To Date", "Marketing Type", "Disabled Flag"
]

# Initialize Gemini 1.5 Flash chat model
chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=google_api_key)


# Serving index.html
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map-headers', methods=['POST'])
def map_headers():
    logger.info("Received request to /map-headers")

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty file"}), 400

    try:
        # Read CSV file into DataFrame
        df = pd.read_csv(file)
        actual_headers = df.columns.tolist()
        logger.info(f"Actual headers: {actual_headers}")

        # Prompt Gemini Flash to map headers
        prompt = f"""
            You are a smart data assistant.

            Map each of the following headers to the most appropriate header from the template list.

            Template headers:
            {TEMPLATE_HEADERS}

            Headers to map:
            {actual_headers}

            Respond with a valid JSON object like:
            {{ "original_header": "mapped_template_header", ... }}
            Only use headers from the template list as values.
        """

        response = chat([HumanMessage(content=prompt)])
        logger.info(f"Gemini Flash response:\n{response.content}")

        # Parse header mapping
        json_match = re.search(r'\{[\s\S]*\}', response.content)
        if not json_match:
            raise ValueError("Gemini response does not contain valid JSON")

        header_mapping = json.loads(json_match.group(0))
        logger.info(f"Parsed mapping: {header_mapping}")

        # Identify unmatched columns
        matched_columns = set(header_mapping.keys())
        unmatched_columns = [col for col in actual_headers if col not in matched_columns]

        # Append unmatched columns to the DataFrame
        for col in unmatched_columns:
            header_mapping[col] = col  

        # Rename headers
        df.rename(columns=header_mapping, inplace=True)

        # Reorder columns according to TEMPLATE_HEADERS + unmatched columns
        mapped_columns = [col for col in TEMPLATE_HEADERS if col in df.columns]
        final_columns = mapped_columns + unmatched_columns
        df = df[final_columns]

        # Write mapped DataFrame to CSV
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)

        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name='mapped_headers.csv'
        )

    except Exception as e:
        logger.exception("Failed to map headers")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting Flask app on port 3333")
    app.run(host="0.0.0.0", debug=True, port=3333)
