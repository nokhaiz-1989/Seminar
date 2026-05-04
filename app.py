import streamlit as st
import requests
import json
import pandas as pd
import time

# -------------------------
# CONFIG (PUT YOUR URL HERE)
# -------------------------
APPS_SCRIPT_URL = "https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec"

# -------------------------
# PAGE SETUP
# -------------------------
st.set_page_config(page_title="Research in One Word", layout="wide")

st.title("🌍 Research in One Word")
st.write("Scan, submit, and watch ideas grow live")

# -------------------------
# SUBMIT WORD SECTION
# -------------------------
st.subheader("✍️ Submit Your Word")

word = st.text_input("Enter ONE adjective about research:", "")

if st.button("Submit 🚀"):
    if word.strip() == "":
        st.error("Please enter a word first.")
    else:
        payload = {
            "word": word.strip()
        }

        try:
            response = requests.post(
                APPS_SCRIPT_URL,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                st.success("Word sent successfully!")
            else:
                st.error(f"Failed to send. Status code: {response.status_code}")

        except Exception as e:
            st.error(f"Error: {e}")

# -------------------------
# LOAD DATA FROM GOOGLE SHEETS (CSV EXPORT METHOD)
# -------------------------
st.subheader("☁️ Live Word Cloud")

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/gviz/tq?tqx=out:csv"

try:
    df = pd.read_csv(SHEET_CSV_URL)

    if df.empty:
        st.info("No data yet.")
    else:
        st.write("### Words collected so far:")
        st.dataframe(df)

        # simple word frequency display
        if "word" in df.columns:
            st.write("### Word Frequency")
            st.bar_chart(df["word"].value_counts())

except Exception as e:
    st.warning("Unable to load data from Google Sheets")
    st.text(str(e))

# -------------------------
# AUTO REFRESH
# -------------------------
time.sleep(5)
st.rerun()
