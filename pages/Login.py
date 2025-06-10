import streamlit as st
from Auth import authenticate_user

def login_page(cookies):
    st.title("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate_user(email, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["username"] = user["username"]
            st.session_state["user_id"] = user["user_id"] # <--- IMPORTANT: Set user_id here
            st.session_state["page"] = "Analyze"

            cookies["logged_in"] = "True"
            cookies["username"] = user["username"]
            cookies["user_id"] = user["user_id"] # <--- Also save to cookies
            cookies["page"] = "Analyze"
            cookies.save()

            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid email or password")
