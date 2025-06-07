import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import streamlit as st

def save_to_sheet(topic, keywords, post_text, image_url, url):
    # 認證與串接 Google Sheet
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["GSPREAD_CREDENTIALS"], scope)
    client = gspread.authorize(creds)

    # 開啟試算表與工作表
    sheet = client.open_by_key(st.secrets["SHEET_ID"])
    worksheet = sheet.sheet1

    # 寫入一列資料
    worksheet.append_row([
        str(datetime.datetime.now()),
        topic,
        keywords,
        post_text,
        image_url,
        url
    ])

