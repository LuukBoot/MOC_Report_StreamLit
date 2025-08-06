import streamlit as st
from streamlit_oauth import OAuth2Component
import json

# Configure the page
st.set_page_config(page_title="Secure MOC Report App", page_icon="🔒", layout="wide")

# Define allowed users (whitelist)
ALLOWED_USERS = [
    "user1@example.com",
    "user2@company.com",
    # Add your allowed email addresses here
]

def get_oauth_component():
    """Initialize and return OAuth2 component"""
    try:
        # Get OIDC configuration from secrets
        client_id = st.secrets["connections"]["gcs"]["client_id"]
        client_secret = st.secrets["connections"]["gcs"]["client_secret"]
        redirect_uri = st.secrets["connections"]["gcs"]["redirect_uri"]
        
        # Create OAuth2 component
        oauth2 = OAuth2Component(
            client_id=client_id,
            client_secret=client_secret,
            authorize_endpoint="https://accounts.google.com/o/oauth2/auth",
            token_endpoint="https://oauth2.googleapis.com/token",
            refresh_token_endpoint="https://oauth2.googleapis.com/token",
            revoke_token_endpoint="https://oauth2.googleapis.com/revoke",
        )
        
        return oauth2
        
    except KeyError as e:
        st.error(f"Missing configuration in secrets: {str(e)}")
        st.error("Please check your `.streamlit/secrets.toml` file.")
        st.stop()
    except Exception as e:
        st.error(f"OAuth configuration error: {str(e)}")
        st.stop()

def get_user_info(access_token):
    """Get user information from Google API"""
    import requests
    
    try:
        # Get user info from Google
        response = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to get user information")
            return None
            
    except Exception as e:
        st.error(f"Error getting user info: {str(e)}")
        return None

def show_login_page():
    """Display the login page"""
    st.title("🔒 MOC Report Application")
    st.markdown("### Secure Access Required")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info("Please log in with your Google account to access the application.")
        st.markdown("Only authorized users can access this application.")
        
        # OAuth login
        oauth2 = get_oauth_component()
        
        result = oauth2.authorize_button(
            name="Login with Google",
            icon="https://developers.google.com/identity/images/g-logo.png",
            redirect_uri=st.secrets["connections"]["gcs"]["redirect_uri"],
            scope="openid email profile",
            key="google_oauth"
        )
        
        if result:
            st.session_state.token = result.get('token')
            st.experimental_rerun()
        
        # Login configuration display (without sensitive data)
        with st.expander("ℹ️ Authentication Info"):
            st.write("- Authentication: Google OpenID Connect")
            st.write("- Authorization: Email whitelist")
            st.write("- Security: OAuth 2.0 with HTTPS")

def main():
    """Main application logic"""
    
    # Check if user is authenticated
    if 'token' in st.session_state and 'user_info' not in st.session_state:
        # Get user information
        user_info = get_user_info(st.session_state.token['access_token'])
        if user_info:
            st.session_state.user_info = user_info
    
    if 'user_info' in st.session_state:
        user_info = st.session_state.user_info
        user_email = user_info.get('email', '')
        user_name = user_info.get('name', 'Unknown User')
        
        # Check if user email is in allowed list
        if user_email not in ALLOWED_USERS:
            st.error("Access denied")
            st.error(f"User {user_email} is not authorized to access this application.")
            st.info("Please contact your administrator for access.")
            
            # Logout button for unauthorized users
            if st.button("🚪 Logout", type="secondary"):
                # Clear session
                for key in ['token', 'user_info']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.experimental_rerun()
            st.stop()
        
        # User is authenticated and authorized
        st.success(f"Welcome, {user_name}! ({user_email})")
        
        # Main application content
        st.title("🔒 Secure MOC Report Application")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("User Information")
            st.write(f"**Name:** {user_name}")
            st.write(f"**Email:** {user_email}")
            if user_info.get('picture'):
                st.image(user_info['picture'], width=100)
        
        with col2:
            st.subheader("Application Features")
            st.write("✅ Secure Google OIDC Authentication")
            st.write("✅ User Authorization Whitelist")
            st.write("✅ Protected Content Access")
        
        st.markdown("---")
        
        # Add your main application content here
        st.subheader("📊 MOC Report Dashboard")
        st.info("This is where your main application content would go.")
        
        # Example content tabs
        tab1, tab2, tab3 = st.tabs(["📈 Reports", "⚙️ Settings", "👥 Users"])
        
        with tab1:
            st.write("### Report Generation")
            st.write("- Data visualization tools")
            st.write("- Custom report templates")
            st.write("- Export functionality")
            
            # Example chart
            try:
                import numpy as np
                chart_data = np.random.randn(20, 3)
                st.line_chart(chart_data)
            except ImportError:
                st.info("Install numpy for chart visualization: `pip install numpy`")
        
        with tab2:
            st.write("### Application Settings")
            st.write("- User preferences")
            st.write("- Report configurations")  
            st.write("- System settings")
            
            # Example settings
            st.checkbox("Enable email notifications", value=True)
            st.selectbox("Report format", ["PDF", "Excel", "CSV"])
        
        with tab3:
            st.write("### User Management")
            st.write("**Authorized Users:**")
            for i, email in enumerate(ALLOWED_USERS, 1):
                st.write(f"{i}. {email}")
        
        # Logout option
        st.markdown("---")
        if st.button("🚪 Logout", type="secondary"):
            # Clear session
            for key in ['token', 'user_info']:
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_rerun()
    
    else:
        # User not authenticated - show login page
        show_login_page()

if __name__ == "__main__":
    main()
