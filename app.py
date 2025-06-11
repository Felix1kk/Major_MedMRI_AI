import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
import json
from firebase_admin import credentials, firestore
from firebase_init import db

st.set_page_config(page_title="MedMRI AI", page_icon="🧠", layout="centered")

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
    /* #MainMenu {
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

# Persistent cookies for login state
cookies = EncryptedCookieManager(prefix="medmri", password="secure-app-password")
if not cookies.ready():
    st.stop()

# Load persistent state from cookies
st.session_state["logged_in"] = cookies.get("logged_in", "False") == "True"
st.session_state["username"] = cookies.get("username", "")
st.session_state["page"] = cookies.get("page", "Login")
st.session_state["user_id"] = cookies.get("user_id", "") # Added user_id

# Routing
page = st.session_state["page"]

if page == "Login":
    from pages.Login import login_page
    login_page(cookies)
elif page == "Register":
    from pages.Register import register_page
    register_page(cookies)
elif page == "Analyze":
    from pages.Analyze import analyze_page
    analyze_page(cookies)
elif page == "My Reports": # New page
    from pages.saved_reports import my_reports_page
    my_reports_page()
elif page == "Help":
    from pages.Help import help_page
    help_page()
elif page == "About":
    from pages.About import about_page
    about_page()
#elif page == "Assistant":
   # from pages.Assistant import assistant_page
   # assistant_page()

with st.sidebar:
    st.title("🧠 MedMRI AI")
    st.markdown(f"👋 Welcome, **{st.session_state.get('username', 'Guest')}**")

    if st.session_state.get("logged_in"):
        nav_options_logged_in = ["Analyze", "My Reports", "Help", "About"]
        nav = st.radio("Go to", nav_options_logged_in, index=nav_options_logged_in.index(st.session_state["page"]))
        if nav != st.session_state["page"]:
            st.session_state["page"] = nav
            cookies["page"] = nav
            cookies.save()
            st.rerun()
    else:
        nav_options_not_logged_in = ["Login", "Register", "Help", "About"]
        nav = st.radio("Go to", nav_options_not_logged_in, index=nav_options_not_logged_in.index(st.session_state["page"]))
        if nav != st.session_state["page"]:
            st.session_state["page"] = nav
            cookies["page"] = nav
            cookies.save()
            st.rerun()

    if st.session_state.get("logged_in") and st.button("Logout"):
        # --- FIX: Explicitly set session state variables instead of clear() ---
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.session_state["user_id"] = ""
        st.session_state["page"] = "Login" # Directly set the page to Login

        # Update cookies as well
        cookies["logged_in"] = "False"
        cookies["username"] = ""
        cookies["user_id"] = ""
        cookies["page"] = "Login"
        cookies.save()

        st.rerun()
