import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
from urllib.parse import urlparse, parse_qs

def get_sheet_id(url):
    # 從 URL 擷取 Google Sheet 的 ID
    parsed = urlparse(url)
    if "/d/" in parsed.path:
        return parsed.path.split("/d/")[1].split("/")[0]
    return None

def add_row_to_gsheet(row_data):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)

    sheet_id = get_sheet_id(st.secrets["GSHEET_URL"])
    sheet = client.open_by_key(sheet_id).sheet1
    sheet.append_row(row_data, value_input_option="USER_ENTERED")

