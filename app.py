import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

#st.set_page_config(page_title="MedMRI AI", page_icon="🧠", layout="centered")

# Persistent cookies for login state
cookies = EncryptedCookieManager(prefix="medmri", password="secure-app-password")
if not cookies.ready():
    st.stop()

# Load persistent state from cookies
st.session_state["logged_in"] = cookies.get("logged_in", "False") == "True"
st.session_state["username"] = cookies.get("username", "")
st.session_state["page"] = cookies.get("page", "Login")

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

# Sidebar Nav
with st.sidebar:
    st.title("🧠 MedMRI AI")
    st.markdown(f"👋 Welcome, **{st.session_state.get('username', 'Guest')}**")

    if st.session_state.get("logged_in"):
        nav = st.radio("Go to", ["Analyze","My Reports", "Help", "About"], index=["Analyze","My Reports", "Help", "About"].index(st.session_state["page"]))
        if nav != st.session_state["page"]:
            st.session_state["page"] = nav
            cookies["page"] = nav
            cookies.save()
            st.rerun()
    else:
        nav = st.radio("Go to", ["Login", "Register", "Help", "About"], index=["Login", "Register", "Help", "About"].index(st.session_state["page"]))
        if nav != st.session_state["page"]:
            st.session_state["page"] = nav
            cookies["page"] = nav
            cookies.save()
            st.rerun()

    if st.session_state.get("logged_in") and st.button("Logout"):
        st.session_state.clear()
        cookies["logged_in"] = "False"
        cookies["username"] = ""
        cookies["page"] = "Login"
        cookies.save()
        st.rerun()
