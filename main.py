import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from google.auth import default
import json
from flask import Flask, request as flask_request

app = Flask(__name__)

def read_google_sheet(sheet_name, worksheet_name):
    """
    Reads data from a Google Sheet.
    """
    try:
        # Use the service account automatically attached to the Cloud Run service
        credentials, project = default()
        gc = gspread.authorize(credentials)
        
        spreadsheet = gc.open(sheet_name)
        worksheet = spreadsheet.worksheet(worksheet_name)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except gspread.exceptions.SpreadsheetNotFound:
        return f"Error: Spreadsheet '{sheet_name}' not found."
    except gspread.exceptions.WorksheetNotFound:
        return f"Error: Worksheet '{worksheet_name}' not found in spreadsheet '{sheet_name}'."
    except Exception as e:
        return f"An error occurred: {e}"

@app.route("/", methods=["GET"])
def handle_request():
    """
    Cloud Run entry point to read the Google Sheet.
    """
    # Configuration is read from environment variables.
    # Set OPPORTUNITIES_SHEET_NAME and OPPORTUNITIES_WORKSHEET_NAME
    # when you run or deploy this application.
    sheet_name = os.getenv("CAPABILITIES_SHEET_NAME")
    worksheet_name = os.getenv("2025_Closed_Won_11_Jun_2025", "Sheet1")

    if not sheet_name:
        return "Error: Capabilities & Case Studies environment variable not set.", 500

    df = read_google_sheet(sheet_name, worksheet_name)

    if isinstance(df, pd.DataFrame):
        return f"Successfully read data from Google Sheet. Found {len(df)} opportunities."
    else:
        return df

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))