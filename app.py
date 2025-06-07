import streamlit as st
import openai
from utils.gsheet import save_to_sheet
from PIL import Image
from bs4 import BeautifulSoup
import urllib.request

# 初始化 OpenAI API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="AI 社群內容自動生成器", layout="centered")
st.title("🧠 AI 社群圖像與貼文生成器")

# 使用者輸入欄位
topic = st.text_input("輸入主題")
keywords = st.text_input("輸入關鍵字（用逗號分隔）")
url = st.text_input("輸入相關網址（選填）")

# 取得網址內容
def fetch_url_content(url):
    try:
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()
        return text[:2000]
    except:
        return ""

# 主按鈕邏輯
if st.button("🎨 生成圖像與貼文") and (topic or keywords or url):
    with st.spinner("生成中..."):
        url_content = fetch_url_content(url) if url else ""
        full_prompt = f"主題：{topic}\n關鍵字：{keywords}\n{url_content}\n\n請針對上述內容，撰寫一段適合用於社群平台的感性貼文，附上鼓舞人心的語句。"

        # 生成文字貼文
        post_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": full_prompt}]
        )
        post_text = post_response.choices[0].message["content"].strip()

        # 生成圖像
        image_response = openai.Image.create(
            prompt=f"{topic} {keywords}, Pixar style, uplifting, detailed, 4k illustration",
            n=1,
            size="512x512"
        )
        image_url = image_response['data'][0]['url']

        # 顯示圖文
        st.image(image_url, caption="🎨 AI 生成圖像")
        st.text_area("📄 生成貼文內容", value=post_text, height=200)

        # 儲存至 Google Sheets
        save_to_sheet(topic, keywords, post_text, image_url, url)
        st.success("✅ 已儲存到 Google Sheet")

