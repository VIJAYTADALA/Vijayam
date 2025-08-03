import streamlit as st
class Config:
    MONGO_URI = st.secrets["mongo"]["uri"]
    DB_NAME = st.secrets["mongo"]["dbname"]
    COLLECTION_NAME = "donations"
    ITEMS_PER_PAGE = 10
    ADMIN_USERNAME = st.secrets["auth"]["admin_username"]
    ADMIN_PASSWORD = st.secrets["auth"]["admin_password"]
    USER_USERNAME = st.secrets["auth"]["user_username"]
    USER_PASSWORD = st.secrets["auth"]["user_password"]