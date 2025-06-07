import streamlit as st
import datetime
from utils.gsheet import add_row_to_gsheet
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="社群圖文自動產生器", layout="centered")
st.title("📢 社群圖文自動產生器")
st.caption("由 ChatGPT + DALL·E 驅動｜輸入主題與目標對象，即可自動生成圖文內容")

# 使用者輸入
topic = st.text_input("請輸入你要產生的主題（如：預防跌倒、銀髮營養、照護者心理健康）")
audience = st.selectbox("目標對象", ["長者", "照護者", "年輕人", "社工師", "家屬", "大眾"])

# prompt 模板
text_prompt_template = """
你是一位專業的社群行銷文案撰寫者，請依據以下資訊，撰寫一篇適合用於 Facebook 貼文的圖文說明，語氣親切、句子簡短清楚、並以繁體中文輸出。
- 主題：{topic}
- 目標對象：{audience}
- 輸出格式：
【主題】
一段簡短的說明（50字內）
一句鼓舞人心的結語
"""

image_prompt_template = "以 {topic} 為主題，繪製一張皮克斯風格的插畫，風格溫馨、色彩明亮、構圖簡潔。"

if st.button("🚀 產生圖文"):
    if not topic:
        st.warning("請先輸入主題")
        st.stop()

    full_prompt = text_prompt_template.format(topic=topic, audience=audience)

    # 呼叫 ChatGPT 生成貼文內容
    with st.spinner("正在生成貼文內容…"):
        text_response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": full_prompt}]
        )
        post_text = text_response.choices[0].message.content.strip()

    # 呼叫 DALL·E 生成圖片
    with st.spinner("正在生成圖片…"):
        image_response = client.images.generate(
            prompt=image_prompt_template.format(topic=topic),
            n=1,
            size="512x512"
        )
        image_url = image_response.data[0].url

    # 顯示生成結果
    st.success("✅ 生成完成")
    st.image(image_url, caption="AI 生成圖片", use_column_width=True)
    st.text_area("📄 生成的貼文內容", post_text, height=200)

    # 儲存到 Google Sheet
    add_row_to_gsheet([
        datetime.datetime.now().isoformat(),
        topic,
        audience,
        post_text,
        image_url
    ])

