import streamlit as st
from config import Config

def is_admin():
    """Check if the current user is logged in as admin"""
    return st.session_state.get("is_admin", False)


