import streamlit as st
from Auth import register_user

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

def register_page(cookies):
    st.title("📝 Register")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        # --- Add Input Validation Here ---
        if not email:
            st.error("Email cannot be empty.")
            return # Stop execution if email is empty
        if not username:
            st.error("Username cannot be empty.")
            return # Stop execution if username is empty
        if not password:
            st.error("Password cannot be empty.")
            return # Stop execution if password is empty
        # --- End Input Validation ---

        if password != confirm_password:
            st.error("Passwords do not match")
        else:
            success = register_user(email, username, password)
            if success:
                st.success("Registration successful! Please log in.")
                st.session_state["page"] = "Login"
                cookies["page"] = "Login"
                cookies.save()
                st.rerun()
            else:
                # The Auth.py register_user already handles the "email already registered"
                # error and shows a warning. So this 'else' block might be redundant
                # if Auth.py handles all registration failures via st.error/warning.
                # However, it's good to keep it as a fallback for any other potential
                # False returns from register_user.
                st.error("Registration failed. Please try again.")
