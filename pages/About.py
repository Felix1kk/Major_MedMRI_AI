import streamlit as st

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp {padding-top: 0;}
footer .stButton {display: none;}  /* Hide the Streamlit logo */
footer .stMetrics {display: none;}  /* Hide the Streamlit logo */
</style>
"""

# Inject custom CSS
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def about_page():
    st.title("ℹ️ About MedMRI AI")
    st.markdown("""
    **MedMRI AI** is an AI-powered medical imaging tool designed to analyze MRI scans and assist radiologists, students, and healthcare practitioners in identifying abnormalities and generating structured medical reports.

    ### Features
    - 🧠 Multimodal image and prompt-based analysis using Gemini
    - 📝 Auto-generated PDF reports
    - 🎙️ Voice input and interactive follow-up suggestions
    - 🔐 User authentication (Firebase)

    ### Technology Stack
    - Streamlit (UI)
    - Google Gemini (Image + Text Model)
    - Firebase (Auth + optional DB)
    - ReportLab, Pillow, PyDub, FPDF (PDF + audio tools)

    ### Developed For:
    - Final Year Capstone / Research Project
    - Demonstration of applied AI in medicine

    > This project is for educational purposes only and not intended for clinical diagnosis.
    """)

