import streamlit as st
import pandas as pd
from bson import ObjectId

class DonationView:
    @staticmethod
    def display(donations, is_admin=False, db=None):
        """Display donation records with edit and delete actions if admin"""
        if not donations:
            st.info("No donation records found matching your criteria.")
            return None, None  # Return both edit_data and delete_ids

        df = pd.DataFrame(donations)
        df['_id'] = df['_id'].astype(str)
        
        if is_admin:
            # Initialize return values
            edit_data = None
            delete_ids = []
            
            st.write("Manage Donations:")
            
            # Create a container for each donation with edit and delete options
            for _, row in df.iterrows():
                with st.container():
                    cols = st.columns([4, 2, 2, 2])
                    
                    # Display donation info
                    with cols[0]:
                        st.write(f"**{row['donor_name']}**")
                        st.write(f"₹{row['donation_amount']:.2f} on {pd.to_datetime(row['donation_date']).strftime('%d-%b-%Y')}")
                        if row['notes']:
                            st.caption(f"Notes: {row['notes']}")
                    
                    # Edit button
                    with cols[1]:
                        if st.button("✏️ Edit", key=f"edit_{row['_id']}"):
                            edit_data = {
                                '_id': row['_id'],
                                'donor_name': row['donor_name'],
                                'donation_amount': row['donation_amount'],
                                'donation_date': pd.to_datetime(row['donation_date']),
                                'notes': row['notes']
                            }
                    
                    # Delete checkbox
                    with cols[2]:
                        if st.checkbox("🗑️ Delete", key=f"del_{row['_id']}"):
                            delete_ids.append(row['_id'])
                    
                    # Add some visual separation
                    st.markdown("---")
            
            return edit_data, delete_ids
        else:
            # Regular user view
            display_df = df.drop(columns=['_id', 'created_at', 'created_by'])
            display_df['donation_amount'] = display_df['donation_amount'].apply(lambda x: f"₹{x:.2f}")
            display_df['donation_date'] = display_df['donation_date'].apply(lambda x: pd.to_datetime(x).strftime('%d-%b-%Y'))
            
            st.table(display_df)
            
            # Excel export
            csv = display_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download as Excel",
                data=csv,
                file_name='donations.csv',
                mime='text/csv'
            )
            return None, None