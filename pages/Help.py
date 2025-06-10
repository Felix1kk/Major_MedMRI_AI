import streamlit as st

def help_page():
    st.title("❓ Help & Instructions")
    st.markdown("""
    ### How to Use MedMRI AI

    1. **Login or Register** with your credentials.
    2. Navigate to **MRI Analysis** page.
    3. Upload one or more MRI images (`.jpg`, `.jpeg`, `.png`).
    4. Add a prompt (or use voice input) to describe what you want to analyze.
    5. Click **Analyze** to view results.
    6. Download the full report as a PDF.

    ### Recommendations
    - Upload high-resolution images for better analysis.
    - Do not upload personally identifiable or sensitive patient data.
    - Use this tool as a **support system**, not a diagnostic substitute.

    ### Troubleshooting
    - 🔐 If login fails, double-check your credentials.
    - 🖼️ If image upload fails, ensure the format is correct.
    - 🌐 Make sure you're connected to the internet for analysis.
    """)
