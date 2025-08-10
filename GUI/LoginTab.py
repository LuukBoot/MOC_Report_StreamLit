import streamlit as st


def show_login_tab():
    """Display the Login tab with basic information."""
    
    st.header("🔐 Login")
    
    # Login form
    with st.form("login_form"):
        st.subheader("User Authentication")
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        submitted = st.form_submit_button("Login", use_container_width=True)
        
        if submitted:
            # Simple authentication (you can enhance this with real authentication)
            if username and password:
                if username == "admin" and password == "password":  # Demo credentials
                    st.success(f"✅ Welcome, {username}!")
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                else:
                    st.error("❌ Invalid credentials. Please try again.")
            else:
                st.warning("⚠️ Please enter both username and password.")
    
    # Information section
    st.divider()
    
    st.subheader("📋 Tab Information")
    st.info("""
    **Login Tab Features:**
    - Simple user authentication
    - Session management
    - Access control for the application
    
    **Demo Credentials:**
    - Username: `admin`
    - Password: `password`
    """)
    
    # System status
    st.subheader("🖥️ System Status")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("System Status", "Online", "🟢")
    
    with col2:
        logged_in_status = "Yes" if st.session_state.get('logged_in', False) else "No"
        st.metric("Logged In", logged_in_status)
    
    with col3:
        current_user = st.session_state.get('username', 'Guest')
        st.metric("Current User", current_user)


if __name__ == "__main__":
    show_login_tab()
