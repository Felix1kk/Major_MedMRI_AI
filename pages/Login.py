import streamlit as st
from Auth import authenticate_user

hide_streamlit_style = """
<style>
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp {padding-top: 0;}
footer .stButton {display: none;}  /* Hide the Streamlit logo */
footer .stMetrics {display: none;}  /* Hide the Streamlit logo */
</style>
"""

# Inject custom CSS
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def login_page(cookies):
    st.title("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # pages/Login.py
import streamlit as st
from Auth import authenticate_user

def login_page(cookies):
    st.title("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # --- Add Input Validation Here ---
        if not email:
            st.error("Email cannot be empty.")
            return # Stop execution if email is empty
        if not password:
            st.error("Password cannot be empty.")
            return # Stop execution if password is empty
        # --- End Input Validation ---

        user = authenticate_user(email, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["username"] = user["username"]
            st.session_state["user_id"] = user["user_id"]
            st.session_state["page"] = "Analyze"

            cookies["logged_in"] = "True"
            cookies["username"] = user["username"]
            cookies["user_id"] = user["user_id"]
            cookies["page"] = "Analyze"
            cookies.save()

            st.success("Login successful!")
            st.rerun()
        else:
            # This error message will be shown if authentication fails
            # (e.g., incorrect email/password, or if authenticate_user returns None
            # due to an error it already logged).
            st.error("Invalid email or password")
    
