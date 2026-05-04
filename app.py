import streamlit as st
import requests
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import qrcode

# 🔁 PASTE YOUR LINKS HERE
WEB_APP_URL = "PASTE_GOOGLE_SCRIPT_URL"
SHEET_CSV = "PASTE_CSV_LINK"
APP_URL = "WILL_ADD_LATER"

st.set_page_config(page_title="Research Cloud", layout="wide")

st.title("🌍 Research in One Word")
st.write("Submit one adjective and watch the live cloud grow!")

col1, col2 = st.columns([1,2])

# QR (temporary placeholder)
qr = qrcode.make("Coming soon")

with col1:
    st.subheader("📱 Scan to Join")
    st.image(qr)

with col2:
    word = st.text_input("Enter ONE word:")

    if st.button("Submit"):
        if word:
            requests.post(WEB_APP_URL, json={"word": word})
            st.success("Submitted!")

st.subheader("☁️ Live Word Cloud")

try:
    df = pd.read_csv(SHEET_CSV)
    words = df["Word"].dropna().tolist()

    if words:
        text = " ".join(words)
        wc = WordCloud(width=1000, height=400).generate(text)

        fig, ax = plt.subplots()
        ax.imshow(wc)
        ax.axis("off")
        st.pyplot(fig)

except:
    st.warning("Waiting for responses...")

st.button("🔄 Refresh")