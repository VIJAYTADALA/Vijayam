import streamlit as st
from database import Database
from auth import is_admin
from admin import adminPage
from homePage import homePage
from database import get_db

def main():
    # Set page configuration
    st.set_page_config(page_title="donations", layout="wide")
    db = get_db()
    if is_admin():
        adminPage()
    else:
        homePage()

if __name__ == "__main__":
    if "page" not in st.session_state:
        st.session_state.page = 1
    
    main()
    