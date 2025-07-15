import streamlit as st
import sys
import os
import json

# Adjusting sys.path to ensure imports work correctly based on the new structure
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rag_pipeline import answer_query
from backend.ingest_scraped import store_scraped_data_in_chroma

st.set_page_config(page_title="Tech QA Bot", page_icon="💬")

st.title("💬 Tech Community QA Bot")

# Source selection
source_option = st.selectbox(
    "Select data source:",
    ("All (Stack Overflow + Reddit)", "Stack Overflow", "Reddit")
)

# Map selected option to internal source parameter
selected_source = "all"
if source_option == "Stack Overflow":
    selected_source = "stackoverflow"
elif source_option == "Reddit":
    selected_source = "reddit"

# Ingest data based on selection
with st.spinner(f"Ingesting data from {source_option}..."):
    # The management of deleting/creating the collection will be handled
    # within store_scraped_data_in_chroma to ensure it's done correctly
    # before adding documents.
    store_scraped_data_in_chroma(tag="python", n=20, source=selected_source)
    st.success(f"Data ingested from {source_option}!")


query = st.text_input("Ask your programming question:")

if query:
    with st.spinner("Finding best answer..."):
        answer = answer_query(query)
        st.markdown("### 🧠 Answer")
        st.markdown(answer)