import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langdetect import detect
import google.generativeai as genai

from utils.parsing import parse_user_query
from utils.filtering import apply_filters

# 1. Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. Load Gemini model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# 3. Page config
st.set_page_config(page_title="Mikro-RAG", page_icon="🚌", layout="wide")

st.title("🚌 Mikro-RAG")
st.markdown("Bildiğini söyler!")

# 4. Load dataset
@st.cache_data
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/yourdocumentabc/export?format=csv"
    return pd.read_csv(sheet_url)

df = load_data()

# 5. Show dataset preview
st.subheader("📄 Veritabanı (Örnek Seferler)")
st.dataframe(df, use_container_width=True)

# 6. User input
st.markdown("✍️ Sorunu buraya yaz:")
user_question = st.text_input(" ", placeholder="örn: en sık sefer sayısı hangisidir")

if user_question:
    # 7. Parse + Filter
    filters = parse_user_query(user_question)
    filtered_df = apply_filters(df, filters)

    st.subheader("🔍 Filtrelenmiş Seferler")
    if filtered_df.empty:
        st.warning("Uygun sefer bulunamadı.")
    else:
        st.dataframe(filtered_df, use_container_width=True)

        # 8. Language detection and prompt
        language = detect(user_question)
        sample_table = filtered_df.to_string(index=False)

        if language == 'tr':
            prompt = f"""
        Kullanıcının sorusu:
        \"\"\"{user_question}\"\"\".

        Aşağıdaki tablo filtrelenmiş veriyi içeriyor. Bu tabloyu analiz et ve sadece tabloya dayalı, kısa, açık ve veri odaklı bir cevap üret.

        Kurallar:
        - Tabloyu tekrar etme.
        - Bilinmeyen bilgi uydurma.
        - Kullanıcının sorusuyla doğrudan ilgili veriyi yorumla.
        - Ekstra öneri, özet veya açıklama verme.
        - En fazla 3 cümle yaz.
        - Sadece kullanıcıya gerekli bilgiyi özetle.

        Tablo:
        {sample_table}
        """
        else:
            prompt = f"""
        User's question:
        \"\"\"{user_question}\"\"\".

        The table below contains filtered trip data. Analyze the table and provide a short, factual, and data-focused answer based only on the table.

        Rules:
        - Do not repeat the table.
        - Do not hallucinate unknown facts.
        - Directly address what the user asked.
        - Do not add extra commentary, summary, or context.
        - Max 3 sentences.
        - Only summarize what matters.

        Table:
        {sample_table}
        """


        # 9. Gemini response
        with st.spinner("Gemini yanıt üretiyor..."):
            response = model.generate_content(prompt)

        st.subheader("🤖 Gemini Yanıtı")
        st.markdown(response.text)
