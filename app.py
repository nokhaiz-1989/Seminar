import streamlit as st
import requests
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import qrcode
from io import BytesIO
import time

# =========================
# 🔗 CONFIG (FILL THESE)
# =========================

WEB_APP_URL = "PASTE_YOUR_GOOGLE_APPS_SCRIPT_URL"
SHEET_CSV = "PASTE_YOUR_GOOGLE_SHEET_CSV_LINK"
APP_URL = "PASTE_YOUR_STREAMLIT_APP_URL"

# =========================
# PAGE SETUP
# =========================

st.set_page_config(page_title="Research Word Cloud", layout="wide")

st.markdown(
    "<h1 style='text-align:center;'>🌍 Research in One Word</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>Scan, submit, and watch ideas grow live</p>",
    unsafe_allow_html=True
)

# =========================
# AUTO REFRESH (every 5 sec)
# =========================

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh > 5:
    st.session_state.last_refresh = time.time()
    st.rerun()

# =========================
# GOOGLE SHEETS POST
# =========================

def send_word(word):
    try:
        requests.post(
            WEB_APP_URL,
            json={"word": word},
            timeout=5
        )
        return True
    except:
        return False

# =========================
# QR CODE GENERATOR
# =========================

def generate_qr(url):
    qr = qrcode.make(url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    return buf.getvalue()

# =========================
# LAYOUT
# =========================

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📱 Join Live")

    if APP_URL != "PASTE_YOUR_STREAMLIT_APP_URL":
        st.image(generate_qr(APP_URL))
    else:
        st.warning("Add your Streamlit URL to generate QR")

    st.caption("Scan to participate")

with col2:
    st.subheader("✍️ Submit Your Word")

    word = st.text_input("Enter ONE adjective about research:")

    if st.button("Submit 🚀"):
        if word:
            success = send_word(word)
            if success:
                st.success("Submitted successfully!")
            else:
                st.error("Failed to send. Try again.")

# =========================
# WORD CLOUD SECTION
# =========================

st.markdown("---")
st.subheader("☁️ Live Word Cloud")

try:
    df = pd.read_csv(SHEET_CSV)

    words = df["Word"].dropna().astype(str).tolist()

    if len(words) > 0:
        text = " ".join(words)

        wc = WordCloud(
            width=1200,
            height=500,
            background_color="black",
            colormap="cool"
        ).generate(text)

        fig, ax = plt.subplots()
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")

        st.pyplot(fig)

        st.caption(f"Total responses: {len(words)}")

    else:
        st.info("Waiting for responses...")

except:
    st.warning("Unable to load data from Google Sheets")

# =========================
# MANUAL REFRESH BUTTON
# =========================

st.button("🔄 Refresh Now")
