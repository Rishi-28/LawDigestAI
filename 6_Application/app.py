import streamlit as st
import time
import sys
import os

# Dynamically add the 5_Analysis directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../5_Analysis')))
from model_output_func import generate_catchphrases, classify_citation

# Title
st.title("LawDigestAI")

# Define Tabs
tabs = st.tabs(["Catchphrase Extraction", "Citation Classification"])

# Catchphrase Extraction Tab
with tabs[0]:
    st.header("Catchphrase Extraction")
    user_input = st.text_area("Enter the case document text:")
    if st.button("Run Catchphrase Extraction Model"):
        with st.spinner("Processing..."):
            progress_bar = st.progress(0)

            # Model
            model_path = os.path.abspath("./2_Generation/catchphrase_Extraction/t5-catchphrase-extraction-model")
            predicted_phrases = generate_catchphrases(str(user_input), model_path)

            for i in range(100):
                time.sleep(0.01)  # Simulated delay
                progress_bar.progress(i + 1)

        st.success("Processing complete!")

        st.subheader("Extracted Catchphrases:")
        for phrase in predicted_phrases:
            st.info(phrase)

# Citation Classification Tab
with tabs[1]:
    st.header("Citation Classification")
    user_input = st.text_area("Enter the citance text:")

    if st.button("Run Citation Classification Model"):
        with st.spinner("Processing..."):
            progress_bar = st.progress(0)

            # Model
            model_path = os.path.abspath("./2_Generation/citation_classification/legalbert-citation-classification-model")
            predicted_citation = classify_citation(user_input, model_path)

            for i in range(100):
                time.sleep(0.01)  # Simulated delay
                progress_bar.progress(i + 1)

        st.success("Processing complete!")
        st.subheader("Citation Class:")
        st.info(predicted_citation)
