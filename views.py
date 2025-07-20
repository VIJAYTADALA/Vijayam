import streamlit as st
import pandas as pd

class DonationView:
    @staticmethod
    def display(donations, is_admin=False):
        """Display donation records"""
        if donations:
            df = pd.DataFrame(donations)
            
            # Convert _id to string for display purposes
            df['_id'] = df['_id'].astype(str)
            
            # Display the dataframe with some styling
            st.dataframe(
                df.drop(columns=['_id', 'created_at', 'created_by']).style.format({
                    'donation_amount': '₹{:.2f}',
                    'donation_date': lambda x: pd.to_datetime(x).strftime('%d-%b-%Y')
                }),
                height=400
            )
            
            # Excel export button with icon
            st.download_button(
                label="📥 Download as Excel",
                data=df.drop(columns=['_id', 'created_at', 'created_by']).to_csv(index=False).encode('utf-8'),
                file_name='donations.csv',
                mime='text/csv',
                help="Export all filtered records to CSV"
            )
            
            # Return the list of donations for deletion handling
            return donations if is_admin else None
        else:
            st.info("No donation records found matching your criteria.")
            return None