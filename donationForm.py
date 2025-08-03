import streamlit as st
from datetime import datetime


def display_donation_form(donation=None):
    """Display form for adding/editing donations"""
    default_date = datetime.now().strftime("%Y-%m-%d")
    
    with st.form(key="donation_form"):
        cols = st.columns(2)
        donor = cols[0].text_input("Donor Name", value=donation["donor"] if donation else "")
        amount = cols[1].number_input("Amount", min_value=0.0, value=float(donation["amount"]) if donation else 0.0)
        
        date = st.date_input(
            "Donation Date",
            value=datetime.strptime(donation["date"], "%Y-%m-%d") if donation and "date" in donation else datetime.now()
        ).strftime("%Y-%m-%d")
        
        notes = st.text_area("Notes", value=donation["notes"] if donation else "")
        
        submit_button = st.form_submit_button("Save Donation")
        
        if submit_button:
            if not donor:
                st.error("Donor name is required")
                return False
            
            return {
                "donor": donor,
                "amount": amount,
                "date": date,
                "notes": notes
            }
    return None
