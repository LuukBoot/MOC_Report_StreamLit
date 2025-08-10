import streamlit as st
import sys
import os

# Add the GUI directory to the path for imports
sys.path.append(os.path.dirname(__file__))

# Import tab modules
from LoginTab import show_login_tab
from MocRerportTab import show_moc_report_tab


def main():
    """Main application with tabbed interface."""
    
    # Configure the page
    st.set_page_config(
        page_title="MOC Report Generator",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = 'Guest'
    
    # Main title
    st.title("📊 MOC Report Generator")
    st.markdown("*Generate professional PDF reports from MOC trading data*")
    
    # Sidebar status
    with st.sidebar:
        st.header("🔧 System Status")
        
        # Login status
        if st.session_state.get('logged_in', False):
            st.success(f"✅ Logged in as: {st.session_state.get('username', 'Unknown')}")
            if st.button("Logout", use_container_width=True):
                st.session_state['logged_in'] = False
                st.session_state['username'] = 'Guest'
                st.rerun()
        else:
            st.warning("⚠️ Not logged in")
        
        st.divider()
        
        # Quick info
        st.subheader("📋 Application Info")
        st.info("""
        **Features:**
        - User authentication
        - MOC report parsing
        - PDF generation
        - Data visualization
        """)
        
        st.subheader("🏢 About")
        st.write("MOC Report Generator v1.0")
        st.write("Built with Streamlit")
    
    # Create tabs
    tab1, tab2 = st.tabs(["🔐 Login", "📊 MOC Report"])
    
    with tab1:
        show_login_tab()
    
    with tab2:
        show_moc_report_tab()
    
    # Footer
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<p style='text-align: center; color: gray;'>© 2025 MOC Report Generator | Built with ❤️ using Streamlit</p>",
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    main()
