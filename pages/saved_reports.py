import streamlit as st
from firebase_admin import firestore
from datetime import datetime
import base64

# Assume Firebase is already initialized by Auth.py or app.py
db = firestore.client()

def save_report_to_firebase(user_id, image_name, report_text, explanation_text=None, translated_text=None, translated_language=None):
    """
    Saves a report to Firestore.
    Can now optionally save patient explanation and translated report.
    """
    timestamp = datetime.now().isoformat()
    report_entry = {
        "user_id": user_id,
        "image_name": image_name,
        "report_text": report_text,
        "timestamp": timestamp,
        "explanation_text": explanation_text, # New field
        "translated_text": translated_text,   # New field
        "translated_language": translated_language # New field
    }
    try:
        # CRITICAL FIX: db.collection().add() returns a tuple (update_time, DocumentReference)
        # We need to unpack it to get the DocumentReference object.
        update_time, doc_ref = db.collection("reports").add(report_entry)
        return doc_ref.id # Return the ID of the newly created document
    except Exception as e:
        st.error(f"Error saving report to Firebase: {e}")
        return None

def load_saved_reports(user_id):
    """Loads saved reports for a specific user from Firestore."""
    try:
        # Order by timestamp for consistent display
        docs = db.collection("reports").where("user_id", "==", user_id).order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]
    except Exception as e:
        st.error(f"Error loading reports: {e}")
        return []

def delete_report_from_firebase(report_id):
    """Deletes a specific report from Firestore."""
    try:
        db.collection("reports").document(report_id).delete()
        return True
    except Exception as e:
        st.error(f"Error deleting report: {e}")
        return False

# --- New function for a dedicated "My Reports" page ---
def my_reports_page():
    st.title("🗂️ My Saved Reports")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please log in to view your saved reports.")
        return

    reports = load_saved_reports(user_id)

    if not reports:
        st.info("You don't have any saved reports yet. Analyze some MRI scans to save them here!")
        return

    st.write("---")
    for report in reports:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### 🧾 {report.get('image_name', 'N/A')}")
            st.markdown(f"**Saved On:** {datetime.fromisoformat(report.get('timestamp')).strftime('%Y-%m-%d %H:%M:%S')}")
        with col2:
            # Using st.session_state for button visibility to avoid re-rendering issues
            # Initialize state for viewing details if not present
            if f"view_details_{report['id']}" not in st.session_state:
                st.session_state[f"view_details_{report['id']}"] = False

            # Toggle button label based on current state
            view_button_label = "Hide Details" if st.session_state[f"view_details_{report['id']}"] else "View Details"
            if st.button(view_button_label, key=f"view_btn_{report['id']}"):
                st.session_state[f"view_details_{report['id']}"] = not st.session_state[f"view_details_{report['id']}"]
                st.rerun() # Rerun to show/hide expander immediately

            # Initialize state for delete confirmation if not present
            if f"confirm_delete_{report['id']}" not in st.session_state:
                st.session_state[f"confirm_delete_{report['id']}"] = False

            if st.button("Delete", key=f"delete_btn_{report['id']}"):
                if st.session_state.get(f"confirm_delete_{report['id']}", False):
                    # User confirmed deletion
                    if delete_report_from_firebase(report['id']):
                        st.success(f"Report '{report.get('image_name', 'N/A')}' deleted.")
                        # Clear confirmation state and rerun to refresh the list
                        if f"confirm_delete_{report['id']}" in st.session_state:
                            del st.session_state[f"confirm_delete_{report['id']}"]
                        st.rerun()
                    else:
                        st.error("Failed to delete report.")
                else:
                    # First click: ask for confirmation
                    st.warning("Click 'Delete' again to confirm deletion.")
                    st.session_state[f"confirm_delete_{report['id']}"] = True


        # Display report details if the 'view_details' state is True for this report
        if st.session_state.get(f"view_details_{report['id']}", False):
            with st.expander("Report Details", expanded=True): # Keep expanded=True here as the button controls visibility
                st.markdown("#### Original Medical Report")
                st.markdown(report.get('report_text', 'No original report text available.'))

                if report.get('explanation_text'):
                    st.markdown("#### Patient-Friendly Explanation")
                    st.markdown(report['explanation_text'])

                if report.get('translated_text'):
                    st.markdown(f"#### Translated Report ({report.get('translated_language', 'N/A').capitalize()})")
                    st.markdown(report['translated_text'])

        st.markdown("---")

