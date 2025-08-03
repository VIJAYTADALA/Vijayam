import streamlit as st
from config import Config
from donationForm import display_donation_form
from donationsDisplay import display_donations
from header import header
from footer import footer

def homePage():
    """Main function to run the home page"""

    # Display header
    header()


    display_donations()

    # Display footer
    footer()