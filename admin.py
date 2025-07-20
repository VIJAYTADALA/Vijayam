import streamlit as st
import time
from database import Database
from forms import DonationForm

class AdminView:
    def __init__(self, db: Database):
        self.db = db

    def show_admin_panel(self):
        """Display donation form in clean layout"""
        st.header("➕ Add New Donation")
        donation_record = DonationForm.display()
        if donation_record:
            if self.db.insert_donation(donations_record):
                st.success("✅ Donation added successfully!")
                time.sleep(1)
                st.experimental_rerun()

    def handle_deletion(self, donations):
        """Standalone deletion interface"""
        st.header("❌ Delete Donations")
        
        if not donations:
            st.warning("No donations found")
            return
            
        # Create selection options
        options = {
            str(d["_id"]): f"{d['donor_name']} - {d['donation_amount']} on {d['donation_date']}"
            for d in donations
        }
        
        selected = st.selectbox(
            "Select donation to delete:",
            options.keys(),
            format_func=lambda x: options[x]
        )
        
        if st.button("Confirm Deletion", type="primary"):
            if self.db.delete_donation(selected):
                st.success("🗑️ Donation deleted!")
                time.sleep(1)
                st.experimental_rerun()