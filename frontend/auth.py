import streamlit as st
from auth_db import authenticate_user, register_user

def auth_ui():
    st.sidebar.title("🔐 Login / Register")

    mode = st.sidebar.radio("Choose action", ["Login", "Register"])

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if mode == "Register":
        confirm = st.sidebar.text_input("Confirm Password", type="password")
        if st.sidebar.button("Register"):
            if password != confirm:
                st.error("Passwords do not match.")
            elif register_user(username, password):
                st.success("Registration successful! You can now login.")
            else:
                st.error("Username already exists.")

    elif mode == "Login":
        if st.sidebar.button("Login"):
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password.")

# Logout logic
def logout_button():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
