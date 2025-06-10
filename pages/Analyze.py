
# pages/Analyze.py
import streamlit as st
from agents.radiologist_agent import analyze_image
from agents.report_generator_agent import generate_report
from agents.medical_explainer_agent import explain_findings
from utils.voice_input import voice_input_button
from utils.utils import create_pdf, create_translated_pdf # Import the new function
from pages.saved_reports import save_report_to_firebase
from Email import send_report_email_interface
from translate_report import translate_report_ui, translate_text
from io import BytesIO

def analyze_page(cookies):
    st.title("🧠🏥⚕️ MedMRI AI 🤖")
    st.subheader("An AI-Powered MRI Analysis App")

    # Initialize session state variables if they don't exist
    if "analysis_results" not in st.session_state:
        st.session_state["analysis_results"] = [] # Stores a list of dicts for each image
    if "pdf_buffer" not in st.session_state:
        st.session_state["pdf_buffer"] = None
    if "combined_translated_report" not in st.session_state: # To store the translation of all reports
        st.session_state["combined_translated_report"] = ""
    if "translation_language" not in st.session_state:
        st.session_state["translation_language"] = "French" # Default language
    if "all_original_reports_combined" not in st.session_state:
        st.session_state["all_original_reports_combined"] = ""
    if "translated_pdf_buffer" not in st.session_state: # New: To store the translated PDF buffer
        st.session_state["translated_pdf_buffer"] = None


    # --- Enhanced Landing Page/Introduction ---
    st.markdown("""
    Welcome to MedMRI AI! 👋
    This application leverages advanced AI to assist in the detection and classification
    of pathologies and abnormalities in MRI images. Gain detailed medical insights and
    patient-friendly explanations.
    """)

    st.markdown("---") # Visual separator

    st.markdown("### Get Started with Your MRI Analysis")
    st.info("""
    Follow these simple steps to analyze your MRI scans:
    1.  **Upload** one or more MRI images (JPG, JPEG, PNG format).
    2.  **(Optional)** Provide a specific **prompt** to guide the AI's analysis (e.g., "Look for brain tumors," "Identify spinal abnormalities").
    3.  Click the **'Analyze MRI'** button to generate your reports.
    """)

    # --- Input Section (Grouped for Aesthetics) ---
    with st.container(border=True): # Use st.container to group related inputs with a visual border
        st.markdown("#### Upload Scans and Describe Analysis")
        uploaded_images = st.file_uploader(
            "Upload one or more MRI scans",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            help="Select your MRI image files here."
        )

        # Using columns for the voice toggle and text input for better layout
        col_voice, col_prompt = st.columns([0.2, 0.8])
        with col_voice:
            use_voice = st.toggle("Use voice input")
        with col_prompt:
            prompt = voice_input_button() if use_voice else st.text_input(
                "Describe what you'd like to know about the scans",
                placeholder="E.g., 'Analyze for any lesions in the brain'",
                help="Provide context or specific instructions for the AI."
            )

        # Analyze button below the inputs
        if st.button("Analyze MRI", key="analyze_button", type="primary"): # "primary" gives it a highlighted look
            if uploaded_images:
                st.session_state["analysis_results"] = [] # Clear previous results on new analysis
                all_reports_for_translation = [] # Collect all reports for combined translation later

                for idx, image in enumerate(uploaded_images):
                    image_bytes = image.getvalue()
                    image_name = image.name
                    image_mime_type = image.type

                    image_buffer = BytesIO(image_bytes)

                    st.subheader(f"🖼️ Image {idx + 1}: {image_name}")
                    st.image(image_buffer, use_column_width=True, caption=f"Uploaded Image {idx + 1}")

                    with st.spinner(f"Analyzing image {idx + 1}... Please wait, this may take a moment."):
                        findings = analyze_image(image_buffer, prompt, image_mime_type)
                        report = generate_report(findings)
                        patient_friendly_summary = explain_findings(findings, mode="patient")

                    st.session_state["analysis_results"].append({
                        "image_name": image_name,
                        "image_data": image_bytes,
                        "report": report,
                        "explanation": patient_friendly_summary
                    })
                    all_reports_for_translation.append(report)

                    user_id = st.session_state.get("user_id")
                    if user_id:
                        save_report_to_firebase(
                            user_id,
                            image_name,
                            report,
                            explanation_text=patient_friendly_summary,
                            translated_text=None,
                            translated_language=None
                        )
                        st.success(f"Report for {image_name} saved to your history.")

                # After processing all images, generate the combined PDF
                if st.session_state["analysis_results"]:
                    report_texts_for_pdf = [r["report"] for r in st.session_state["analysis_results"]]
                    image_data_for_pdf = [{"data": r["image_data"]} for r in st.session_state["analysis_results"]]
                    pdf_buffer = create_pdf(report_texts_for_pdf, image_data_for_pdf)
                    st.session_state["pdf_buffer"] = pdf_buffer

                    st.session_state["all_original_reports_combined"] = "\n\n--- Next Report ---\n\n".join(all_reports_for_translation)
                    st.session_state["combined_translated_report"] = ""
                    st.session_state["translated_pdf_buffer"] = None
            else:
                st.warning("Please upload at least one MRI scan before analyzing.")
        else:
        # This branch runs if the button was not clicked or no images uploaded
        # Ensure that if a previous analysis exists, results are still displayed.
          pass # The display logic below handles showing results from session_state


    # --- Results Section (only displays if analysis has been run) ---
    if st.session_state["analysis_results"]:
        st.markdown("---") # Separator before results
        st.header("📊 Analysis Results") # Changed to header for prominence

        # Display individual reports and explanations
        for idx, result in enumerate(st.session_state["analysis_results"]):
            st.markdown(f"### 🖼️ Report for {result['image_name']}")
            st.markdown(result["report"])

            with st.expander(f"💬 Explanation for Patients ({result['image_name']})"):
                st.markdown(result["explanation"])
            st.markdown("---") # Separator for clarity between image reports

        # --- Download & Share Combined Report ---
        st.subheader("⬇️ Download & Share Combined Report")
        if st.session_state["pdf_buffer"]:
            st.download_button(
                label="📥 Download Combined Original Report PDF",
                data=st.session_state["pdf_buffer"],
                file_name="MRI_analysis_report_original.pdf",
                mime="application/pdf"
            )
            st.session_state["pdf_buffer"].seek(0)
            send_report_email_interface(st.session_state["pdf_buffer"])
        else:
            st.info("Combined original report PDF not yet generated.")

        # --- Translate Combined Report ---
        st.markdown("---") # Separator before translation
        st.subheader("🌍 Translate Combined Report")

        if st.session_state["all_original_reports_combined"]:
            st.session_state["translation_language"] = st.selectbox(
                "Choose target language:",
                ["French", "Spanish", "German", "Arabic", "Chinese", "Hindi", "Portuguese"],
                key="translate_lang_select",
                index=["French", "Spanish", "German", "Arabic", "Chinese", "Hindi", "Portuguese"].index(st.session_state["translation_language"])
            )

            if st.button("Translate Combined Report", key="translate_combined_btn", type="secondary"): # "secondary" for a slightly less prominent look
                with st.spinner(f"Translating combined report to {st.session_state['translation_language']}..."):
                    translated_text = translate_text(
                        st.session_state["all_original_reports_combined"],
                        st.session_state["translation_language"]
                    )
                    if translated_text:
                        st.session_state["combined_translated_report"] = translated_text
                        st.success("Combined translation complete!")

                        lang_code_map = {
                            "French": "fr", "Spanish": "es", "German": "de",
                            "Arabic": "ar", "Chinese": "zh", "Hindi": "hi", "Portuguese": "pt"
                        }
                        language_code_for_pdf = lang_code_map.get(st.session_state["translation_language"], "en")

                        translated_pdf_buffer = create_translated_pdf(
                            translated_text,
                            language_code_for_pdf
                        )
                        st.session_state["translated_pdf_buffer"] = translated_pdf_buffer

                        user_id = st.session_state.get("user_id")
                        if user_id:
                            save_report_to_firebase(
                                user_id,
                                f"Combined Translated Report ({st.session_state['translation_language']})",
                                st.session_state["all_original_reports_combined"],
                                explanation_text=None,
                                translated_text=translated_text,
                                translated_language=st.session_state["translation_language"]
                            )
                            st.info("Combined translated report saved to your history.")

                    else:
                        st.error("Failed to translate the combined report.")

            if st.session_state["combined_translated_report"]:
                st.subheader("🌍 Combined Translated Report Output")
                st.text_area("Combined Translation", st.session_state["combined_translated_report"], height=600)

                if st.session_state["translated_pdf_buffer"]:
                    st.download_button(
                        label=f"📥 Download Translated Report PDF ({st.session_state['translation_language']})",
                        data=st.session_state["translated_pdf_buffer"],
                        file_name=f"MRI_analysis_report_translated_{st.session_state['translation_language'].lower()}.pdf",
                        mime="application/pdf"
                    )
                    st.session_state["translated_pdf_buffer"].seek(0)
        else:
            st.info("Upload images and click 'Analyze MRI' to generate reports for translation.")
    else: # This else pertains to if st.session_state["analysis_results"] is empty
        # If no analysis has been performed yet, show the initial state with helpful messages
        st.info("No analysis performed yet. Upload MRI scans and click 'Analyze MRI' to begin.")




