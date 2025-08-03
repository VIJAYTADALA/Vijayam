import streamlit as st
from config import Config
from auth import is_admin

def login_form():
    """Display login form as an overlay and handle authentication"""
    show_form = st.session_state.get("show_login_form", False)

    if show_form:
        # Create modal dialog using Streamlit components
        with st.container():
            cols = st.columns([1,3,1])
            with cols[1]:
                with st.container():
                    st.subheader("Admin Login")
                    
                    # Use Streamlit form for better handling
                    with st.form("login_form"):
                        username = st.text_input("Username")
                        password = st.text_input("Password", type="password")
                        submitted = st.form_submit_button("Login")
                        cancelled = st.form_submit_button("Cancel")
                       
                        
                        if submitted:
                            if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
                                st.session_state.is_admin = True
                                st.session_state.show_login_form = False
                                st.success("Logged in as admin")
                                st.experimental_rerun()
                            else:
                                st.error("Invalid credentials")
                        
                        if cancelled:
                            st.session_state.show_login_form = False
                            st.experimental_rerun()
def login_button():
    """Display login button at the top right if user is not logged in"""
    if not is_admin():
        # Position the button using columns
        cols = st.columns([10,1])
        with cols[1]:
            if st.button("Admin Login", key="login_button"):
                st.session_state.show_login_form = True
                st.experimental_rerun()
        
        # Show the overlay form if needed
        if st.session_state.get("show_login_form", False):
            login_form()

def logout_button():
    """Display logout button if user is logged in"""
    if is_admin():
        # Position the button using columns
        cols = st.columns([4,1])
        with cols[1]:
            if st.button("Logout", key="logout_button"):
                st.session_state.is_admin = False
                st.success("Logged out successfully")
                st.experimental_rerun()