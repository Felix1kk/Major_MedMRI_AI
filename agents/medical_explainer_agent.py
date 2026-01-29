import google.generativeai as genai
import streamlit as st

gemini_api_key = st.secrets["gemini"]["api_key"]

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

def explain_findings(findings, mode="technical"):
    if mode == "patient":
        prompt = """
        Please explain the following MRI findings in simple, easy-to-understand language as if you are talking to a patient. Avoid medical jargon. Be clear, empathetic, and reassuring where possible.

        MRI Findings:
        """
    else:
        prompt = """
        Rephrase the following medical MRI findings in a clearer and more structured form suitable for a medical explanation.

        Findings:
        """

    try:
        response = model.generate_content([prompt + findings])
        return response.text.strip()
    except Exception as e:
        return f"Error generating explanation: {str(e)}"
