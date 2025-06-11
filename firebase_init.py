# firebase_init.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

firebase_json=json.loads(st.secrets["firebase"]["json"])
@st.cache_resource
def get_firebase_client():
    """Initializes Firebase and returns the Firestore client, cached."""
    if not firebase_admin._apps:
        try:
            # Access credentials from Streamlit secrets
            cred = credentials.Certificate(firebase_json)
            firebase_admin.initialize_app(cred)
            # st.success("Firebase initialized successfully!") # Optional: for debugging purposes
        except Exception as e:
            st.error(f"Failed to initialize Firebase: {e}. Please ensure your `.streamlit/secrets.toml` is correctly configured.")
            st.stop() # Stop the app if Firebase fails to initialize
    return firestore.client()

# Call the cached function immediately when this module is imported
# This ensures Firebase is initialized and the client is ready
db = get_firebase_client()
