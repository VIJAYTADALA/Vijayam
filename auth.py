from streamlit_authenticator import Authenticate
from config import Config
import streamlit as st
import time

class Auth:
    def __init__(self):
        self.config = Config.get_auth_config()
        self.authenticator = Authenticate(
            self.config["credentials"],
            self.config["cookie_name"],
            self.config["key"],
            self.config["cookie_expiry_days"]
        )
        self._init_session_state()

    def _init_session_state(self):
        """Initialize required session state variables"""
        required_keys = {
            'authentication_status': None,
            'username': None,
            'name': None,
            'logout_clicked': False,
            'login_attempted': False
        }
        
        for key, default_value in required_keys.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

    def login(self):
        """Handle the login process"""
        try:
            if not st.session_state.login_attempted:
                name, authentication_status, username = self.authenticator.login('Login', 'main')
                
                if authentication_status is not None:
                    st.session_state.login_attempted = True
                    
                    if authentication_status:
                        st.session_state.authentication_status = True
                        st.session_state.name = name
                        st.session_state.username = username
                        st.session_state.logout_clicked = False
                        return True
                    else:
                        st.error('Username/password is incorrect')
                
                return False
            return st.session_state.authentication_status
        except Exception as e:
            st.error(f"Login error: {str(e)}")
            return False

    def logout(self):
        """Handle logout process"""
        if st.session_state.get('logout_clicked', False):
            self.authenticator.cookie_manager.delete(self.config["cookie_name"])
            st.session_state.clear()
            st.session_state.logout_clicked = True
            time.sleep(0.1)
            st.experimental_rerun()

    def show_logout_button(self):
        """Display logout button with unique key"""
        if st.sidebar.button("Logout", key="unique_logout_button"):
            st.session_state.logout_clicked = True
            self.logout()

    def check_auth(self):
        """Check authentication status"""
        if st.session_state.get('logout_clicked'):
            st.session_state.login_attempted = False
            return None, None
        
        if st.session_state.get('authentication_status'):
            return st.session_state.name, st.session_state.username
        
        if self.login():
            return st.session_state.name, st.session_state.username
        
        return None, None