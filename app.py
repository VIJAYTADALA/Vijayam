import streamlit as st
from auth import Auth
from database import Database
from admin import AdminView
from user import UserView
from forms import SearchFilters

def main():
    # Initialize services
    auth = Auth()
    db = Database()
    
    # Check authentication
    name, username = auth.check_auth()
    
    # If not authenticated, stop execution
    if name is None or username is None:
        return
    
    # Display user info and logout button
    auth.show_logout_button()
    st.sidebar.write(f"Welcome *{name}*")
    
    is_admin = (username == "admin")
    
    # Navigation system
    if is_admin:
        st.sidebar.title("Admin Navigation")
        admin_page = st.sidebar.radio(
            "Select Function:",
            ["View Donations", "Add Donation", "Delete Donation"],
            index=0
        )
    else:
        admin_page = "View Donations"
    
    # Get common search filters (shown on all pages)
    query = SearchFilters.display()
    donations = db.get_donations(query)
    
    # Show appropriate view based on selection
    if admin_page == "View Donations":
        UserView.show_user_view(donations)
    elif admin_page == "Add Donation":
        AdminView(db).show_admin_panel()
    elif admin_page == "Delete Donation":
        AdminView(db).handle_deletion(donations)
    
    # Clean up
    db.close()

if __name__ == "__main__":
    main()