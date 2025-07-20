import streamlit as st

class Config:
    @staticmethod
    def get_mongo_config():
        return {
            "uri": st.secrets["mongo"]["uri"],
            "dbname": st.secrets["mongo"]["dbname"]
        }
    
    @staticmethod
    def get_auth_config():
        return {
            "cookie_name": "donation_app",
            "key": "abcdef",
            "cookie_expiry_days": 30,
            "credentials": {
                "usernames": {
                    "admin": {
                        "name": "Admin User",
                        "password": st.secrets["auth"]["admin_password"]
                    },
                    "user": {
                        "name": "Regular User",
                        "password": st.secrets["auth"]["user_password"]
                    }
                }
            }
        }