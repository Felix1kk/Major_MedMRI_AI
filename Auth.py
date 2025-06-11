import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
from firebase_init import db


def register_user(email, username, password):
    hashed_pw = generate_password_hash(password)
    user_ref = db.collection("users").document(email)
    user_ref.set({
        "email": email,
        "username": username,
        "password": hashed_pw,
        "created_at": datetime.utcnow().isoformat()
    })
    return True

def authenticate_user(email, password):
    """Authenticates a user against Firestore."""
    try:
        user_ref = db.collection("users").document(email).get()
        if user_ref.exists:
            user = user_ref.to_dict()
            if check_password_hash(user["password"], password):
                # Add the document ID (which is the email in this case) as user_id to the returned dict
                user["user_id"] = user_ref.id # <--- THIS IS THE CRUCIAL LINE
                return user
        return None # Return None if user does not exist or password does not match
    except Exception as e:
        st.error(f"Error authenticating user: {e}")
        return None

