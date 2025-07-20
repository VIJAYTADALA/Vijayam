from views import DonationView
import streamlit as st

class UserView:
    @staticmethod
    def show_user_view(donations):
        """Display common user functionality"""
        st.header("👀 View Donation Records")
        DonationView.display(donations, is_admin=False)