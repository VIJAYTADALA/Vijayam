from streamlit_authenticator.hasher import Hasher

print(Hasher(['admin123', 'user123']).generate())