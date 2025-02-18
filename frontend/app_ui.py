import streamlit as st
import requests

# ✅ Your Cloud Run API URL
API_URL = "https://arize-rag-57979401749.us-central1.run.app/query"

st.set_page_config(page_title="Network Security Log Analyzer", layout="wide")
st.title("Network Security Log Analyzer 🔍")

st.markdown("Enter a security-related query to analyze network logs for suspicious activity in the Unified Host and Network Dataset, specifically using NetFlow logs from the first 10 days of data collected at Los Alamos National Laboratory (LANL). This dataset captures bidirectional network events, including source/destination devices, ports, protocols, and data transfer patterns. The logs have been de-identified while preserving structural relationships, allowing for security analysis of potential threats like DDoS attacks, unauthorized access, and anomalous traffic patterns. Use this tool to investigate network activity and detect security incidents.")

# User input
query = st.text_input("Enter your query:", placeholder="Has there been a brute force attack?")

if st.button("Analyze Logs"):
    if query:
        with st.spinner("Processing..."):
            response = requests.get(API_URL, params={"query": query})
            if response.status_code == 200:
                data = response.json()
                st.subheader("GPT Analysis:")
                st.write(data["gpt_analysis"])
            else:
                st.error("Error: Could not get a response from the server.")
    else:
        st.warning("Please enter a query.")

st.markdown("---")
st.markdown("Powered by FastAPI, FAISS, and GPT-4 Turbo")
