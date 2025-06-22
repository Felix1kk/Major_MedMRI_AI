import streamlit as st

hide_streamlit_style = """
    <style>
    /* Hide the 'Made with Streamlit' footer badge */
    footer {
        visibility: hidden;
        height: 0%;
    }
    /* Potentially hide the 'Deploy' button/toolbar */
    div[data-testid="stToolbar"] {
        visibility: hidden !important;
        height: 0%;
        position: fixed;
    }
    /* Hide the GitHub icon (if it appears separately from MainMenu) */
    #GithubIcon {
        visibility: hidden;
    }
    /* Hide the main menu (hamburger icon) if desired, but this might hide useful options */
    /* #MainMenu {  <--- COMMENT THIS LINE OUT (or remove it)
        visibility: hidden;
    } */
    /* If you want to hide the 'Manage app' button (on Community Cloud) */
    .stDeployButton {
        visibility: hidden;
        height: 0%;
    }
    </style>
    """
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

