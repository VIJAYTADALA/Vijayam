import streamlit as st
from datetime import datetime
from database import Database
from config import Config
from auth import is_admin
from database import get_db
from searchDonations import show_search_criteria, get_filtered_donations

def display_donations():
    show_search_criteria()
    db= get_db()
    """Display donations with pagination"""
    st.write("Donation Records")
    
    # Pagination
    page = st.number_input("Page", min_value=1, value=1)
    donations, total = get_filtered_donations(page)
    total_pages = (total // Config.ITEMS_PER_PAGE) + 1
    
    if not donations:
        st.info("No donations found")
        return
    
    # Display donations in a table
    for donation in donations:
        cols = st.columns([3, 2, 2, 3, 2,2])
        cols[0].write(donation["donor"])
        cols[1].write(f"${donation['amount']:,.2f}")
        cols[2].write(donation["date"].strftime("%Y-%m-%d") if isinstance(donation["date"], datetime) else donation["date"])
        cols[3].write(donation.get("notes", ""))
        
        # Edit and Delete buttons (admin only)
        if is_admin():
            if cols[4].button("✏️", key=f"edit_{donation['_id']}"):
                st.session_state.editing = str(donation["_id"])
                st.experimental_rerun()
            
            if cols[5].button("🗑️", key=f"delete_{donation['_id']}"):
                if db.delete_donation(str(donation["_id"])):
                    st.success("Donation deleted successfully")
                    st.experimental_rerun()
                else:
                    st.error("Failed to delete donation")
    
    # Pagination controls
    st.write(f"Page {page} of {total_pages} - {total} total donations")
    prev_col, _, next_col = st.columns([1, 8, 1])
    
    if prev_col.button("Previous") and page > 1:
        st.session_state.page = page - 1
        st.experimental_rerun()
    
    if next_col.button("Next") and page < total_pages:
        st.session_state.page = page + 1
        st.experimental_rerun()
