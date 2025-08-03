import streamlit as st
from database import Database
from donationForm import display_donation_form
from database import get_db

def addDonation():
    """Add a new donation"""
    db = get_db()
    st.subheader("Add New Donation")
    if st.button("Cancel"):
        st.session_state.adding = False
        st.experimental_rerun()
    
    form_data = display_donation_form()
    if form_data:
        if db.add_donation(**form_data):
            st.success("Donation added successfully")
            st.session_state.adding = False
            st.experimental_rerun()
        else:
            st.error("Failed to add donation")