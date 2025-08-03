import streamlit as st
from auth import is_admin
from login import login_button, logout_button

def header():
    """Display the header with the app title and logo"""
    # st.markdown(
    #     """
    #     <style>
    #         .header img {
    #             width: 50px;
    #         }
    #     </style>
    #     """,
    #     unsafe_allow_html=True
    # )
    # st.markdown('<div class="header"><img src="https://example.com/logo.png" alt="Logo"><h3>Vijayam</h3></div>', unsafe_allow_html=True)
    if is_admin():
        logout_button()
    else:
        login_button()
    