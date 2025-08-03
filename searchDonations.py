import streamlit as st
from datetime import datetime, timedelta
from config import Config
from auth import is_admin
from database import get_db

def show_search_criteria():
    """Display search criteria options"""
    st.sidebar.header("Search Criteria")
    
    # Default values
    default_from_date = datetime.now() - timedelta(days=100)
    default_to_date = datetime.now()
    
    # Search fields
    donor_name = st.sidebar.text_input("Donor Name", value="Any")
    amount = st.sidebar.text_input("Amount", value="Any")
    from_date = st.sidebar.date_input("From Date", value=default_from_date)
    to_date = st.sidebar.date_input("To Date", value=default_to_date)
    
    # Search button
    if st.sidebar.button("Search"):
        st.session_state.search_params = {
            'donor_name': donor_name,
            'amount': amount,
            'from_date': from_date,
            'to_date': to_date
        }
        st.experimental_rerun()
    
    # Clear button
    if st.sidebar.button("Clear Search"):
        if 'search_params' in st.session_state:
            del st.session_state.search_params
        st.experimental_rerun()

def get_filtered_donations(page=1, per_page=Config.ITEMS_PER_PAGE):
    """Get donations filtered by search criteria"""
    db = get_db()
    
    # Default filter
    filter_query = {}
    
    # Apply search filters if they exist
    if hasattr(st.session_state, 'search_params'):
        params = st.session_state.search_params
        
        # Donor name filter (case insensitive partial match)
        if params['donor_name'].lower() != 'any':
            filter_query['donor'] = {
                '$regex': params['donor_name'],
                '$options': 'i'  # case insensitive
            }
        
        # Amount filter
        if params['amount'].lower() != 'any':
            try:
                amount = float(params['amount'])
                filter_query['amount'] = amount
            except ValueError:
                st.error("Please enter a valid number for amount")
        
        # Date range filter
        filter_query['date'] = {
            '$gte': datetime.combine(params['from_date'], datetime.min.time()),
            '$lte': datetime.combine(params['to_date'], datetime.max.time())
        }
    
    skip = (page - 1) * per_page
    donations = list(db.collection.find(filter_query).skip(skip).limit(per_page))
    total = db.collection.count_documents(filter_query)
    
    return donations, total
