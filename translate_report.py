

def translate_text(original_text, target_language):
    try:
        response = model.generate_content([
            f"Translate the following medical report to {target_language} in accurate medical terminology:",
            original_text
        ])
        return response.text
    except Exception as e:
        st.error(f"Translation failed: {e}")
        return None

def translate_report_ui(report_text):
    st.subheader("🌍 Translate Report")
    language = st.selectbox("Choose target language:", ["French", "Spanish", "German", "Arabic", "Chinese", "Hindi", "Portuguese"], key="translate_lang_select")

    if st.button("Translate Report", key="translate_btn"):
        with st.spinner("Translating report..."):
            translated = translate_text(report_text, language)
            if translated:
                st.session_state["translated_report"] = translated
                st.success("Translation complete!")
