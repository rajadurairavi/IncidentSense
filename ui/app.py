import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(page_title="IncidentSense", layout="centered")

st.title("🧠 IncidentSense – Helix Incident Analyzer")
st.markdown("Paste the incident description from Helix and click **Analyze**.")

description = st.text_area(
    "Incident Description",
    height=200,
    placeholder="Paste full incident details here..."
)

if st.button("Analyze"):
    if not description.strip():
        st.warning("Please provide an incident description.")
    else:
        with st.spinner("Analyzing incident..."):
            payload = {
                "description": description
            }

            response = requests.post(API_URL, json=payload)

            if response.status_code != 200:
                st.error("Error calling backend API.")
            else:
                result = response.json()

                if result.get("based_on_history"):
                    st.subheader("🔍 Root Cause")
                    st.write(result["answer"].split("Resolution Steps:")[0].replace("Root Cause:", "").strip())

                    st.subheader("🛠 Resolution Steps")
                    resolution = result["answer"].split("Resolution Steps:")[-1].strip()
                    st.write(resolution)

                    st.metric("Confidence", result.get("confidence"))
                else:
                    st.warning(result.get("message"))
