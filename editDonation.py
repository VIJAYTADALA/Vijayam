import streamlit as st
from datetime import datetime
from database import get_db
from donationForm import display_donation_form

def editDonation():
    """Edit an existing donation"""
    db= get_db()
    donation_id = st.session_state.editing
    donation = db.get_donation_by_id(donation_id)
    
    if donation:
        st.subheader("Edit Donation")
        if st.button("Cancel"):
            del st.session_state.editing
            st.experimental_rerun()
        
        # Convert date to string if it's a datetime object
        if isinstance(donation["date"], datetime):
            donation["date"] = donation["date"].strftime("%Y-%m-%d")
        
        form_data = display_donation_form(donation)
        if form_data:
            if db.update_donation(donation_id, **form_data):
                st.success("Donation updated successfully")
                del st.session_state.editing
                st.experimental_rerun()
            else:
                st.error("Failed to update donation")
    else:
        st.error("Donation not found")
        del st.session_state.editing
        st.experimental_rerun()