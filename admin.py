import streamlit as st
from donationsDisplay import display_donations
from editDonation import editDonation
from addDonation import addDonation
from header import header
from footer import footer

def adminPage():

    # Display header
    header()
    
    # Add new donation button (admin only)
    if st.button("➕ Add New Donation"):
        st.session_state.adding = True
    
    # Handle adding new donation
    if st.session_state.get("adding"):
        addDonation()
    
    # Handle editing existing donation
    elif st.session_state.get("editing"):
        editDonation()
    
    # Display donations
    display_donations()

    # Display footer
    footer()