import streamlit as st
from datetime import datetime

class DonationForm:
    @staticmethod
    def display():
        st.header("Add Donation Records")
        
        with st.form("donation_form"):
            donor_name = st.text_input("Donor Name", key="donor_name")
            donation_amount = st.number_input("Donation Amount", min_value=0.0, format="%.2f", key="donation_amount")
            donation_date = st.date_input("Donation Date", key="donation_date")
            notes = st.text_area("Notes", key="notes")
            
            submitted = st.form_submit_button("Submit")
            
            if submitted:
                return {
                    "donor_name": donor_name,
                    "donation_amount": donation_amount,
                    "donation_date": donation_date.strftime("%Y-%m-%d"),
                    "notes": notes,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "created_by": st.session_state.get("username")
                }
        return None

class SearchFilters:
    @staticmethod
    def display():
        with st.expander("Search Filters"):
            col1, col2 = st.columns(2)
            with col1:
                donor_filter = st.text_input("Filter by Donor Name")
            with col2:
                amount_filter = st.number_input("Filter by Minimum Amount", min_value=0.0, value=0.0)
            
            col3, col4 = st.columns(2)
            with col3:
                date_from = st.date_input("From Date")
            with col4:
                date_to = st.date_input("To Date")
            
            query = {}
            
            if donor_filter:
                query["donor_name"] = {"$regex": donor_filter, "$options": "i"}
            
            if amount_filter > 0:
                query["donation_amount"] = {"$gte": amount_filter}
            
            if date_from and date_to:
                query["donation_date"] = {
                    "$gte": date_from.strftime("%Y-%m-%d"),
                    "$lte": date_to.strftime("%Y-%m-%d")
                }
            elif date_from:
                query["donation_date"] = {"$gte": date_from.strftime("%Y-%m-%d")}
            elif date_to:
                query["donation_date"] = {"$lte": date_to.strftime("%Y-%m-%d")}
            
            return query