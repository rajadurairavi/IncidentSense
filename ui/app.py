import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(page_title="IncidentSense", layout="centered")

st.title("🧠 IncidentSense – Helix Incident Analyzer")

st.markdown("Paste incident details below and click **Analyze**")

summary = st.text_input("Incident Summary")
description = st.text_area("Incident Description", height=150)

if st.button("Analyze"):
    if not summary or not description:
        st.warning("Please provide both summary and description")
    else:
        with st.spinner("Analyzing incident..."):
            payload = {
                "summary": summary,
                "description": description
            }

            response = requests.post(API_URL, json=payload)

            if response.status_code != 200:
                st.error("Error calling backend API")
            else:
                result = response.json()

                st.subheader("📋 Incident Details")
                st.write(result["incident"])

                if result["based_on_history"]:
                    st.subheader("🔍 Root Cause & Resolution")
                    st.success(result["answer"])
                    st.metric("Confidence", result["confidence"])
                else:
                    st.warning(result["message"])
