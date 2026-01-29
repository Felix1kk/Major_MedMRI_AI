import streamlit as st
import google.generativeai as genai
from PIL import Image # Make sure PIL is imported if you use it elsewhere, though not directly for getvalue()

gemini_api_key = st.secrets["gemini"]["api_key"]

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_image(image_file_buffer, prompt, mime_type): # <--- CORRECTED: Now accepts 'mime_type'
    """
    Analyzes an MRI image using the Gemini model to identify anatomical regions
    and generate a radiologist-style report.

    Args:
        image_file_buffer (io.BytesIO): A BytesIO object containing the image data.
        prompt (str): User's prompt for analysis.
        mime_type (str): The MIME type of the image (e.g., "image/jpeg", "image/png").

    Returns:
        str: A detailed medical report based on the MRI analysis.
    """
    raw_bytes = image_file_buffer.getvalue() # Get raw bytes from the BytesIO buffer

    image_data = {
        "mime_type": mime_type, # Use the passed mime_type directly
        "data": raw_bytes
    }

    # AI Region Identifier prompt
    region_prompt = """
    What anatomical region is shown in this MRI image? Options may include: brain, spine, abdomen, pelvis, cardiac, joints, or whole body.
    Be concise and accurate.
    """

    try:
        region_response = model.generate_content([region_prompt, image_data])
        region = region_response.text.strip()
    except Exception as e:
        region = "Unknown (error identifying region)"
        # You might want to log the error for debugging: print(f"Error identifying region: {e}")

    full_prompt = f"""
    You are an expert radiologist. Carefully analyze this MRI image.
    Anatomical Region: {region}

    Instructions:
    1. Describe notable structures, patterns, or abnormalities.
    2. Identify any pathologies such as tumors, lesions, inflammation, etc.
    3. Suggest possible diagnoses.
    4. Use bullet points and medical terminology.
    """

    try:
        response = model.generate_content([full_prompt, image_data])
        return f"**Detected Region:** {region}\n\n" + response.text.strip()
    except Exception as e:
        return f"❌ Error analyzing image: {str(e)}"
        # You might want to log the error for debugging: print(f"Error during full analysis: {e}")
