import os
import sys
import streamlit as st
from datetime import datetime

# Add the src directory to the path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

try:
    from src.ReportParser import ParsedReport
    from src.PdfCreation import create_trade_report_pdf
    from src.OpenAi import extract_trades_from_rawtext
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please ensure the src directory is properly configured.")
    ParsedReport = None
    create_trade_report_pdf = None


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


def show_moc_report_tab():
    """Display the MOC Report tab with text input and PDF generation."""
    
    # Check if imports are available
    if ParsedReport is None or create_trade_report_pdf is None:
        st.error("❌ Required modules not available. Please check your installation.")
        st.stop()
    
    st.header("📊 MOC Report Generator")
    
    # Check if user is logged in (optional security)
    if not st.session_state.get('logged_in', False):
        st.warning("⚠️ Please login first to access this feature.")
        st.stop()
    
    st.subheader("📝 Report Input")
    st.info("Paste your MOC report text below and click 'Create PDF' to generate a formatted report.")
    
    # Text input area
    report_text = st.text_area(
        "MOC Report Text",
        placeholder="""Date: 2024-01-15

Window dates:
FE  15-16 Jan
MW  17-18 Jan
BE  19-20 Jan

===============================
ULSD 10ppm barges:

Offers: Company A/Company B
Bids: Company C/Company D

Trades:
Trade 1 details here
Trade 2 details here

Average Price: $650.50
Total Volume: 25.0
Total volume this week: 15.0
All volume up till now: 40.0

===============================
50ppm barges:

Offers: Company E
Bids: Company F/Company G

Trades:
Trade 3 details here

Average Price: $645.00
Total Volume: 10.0
Total volume this week: 8.0
All volume up till now: 18.0
""",
        height=300
    )
    
    # PDF generation section
    st.subheader("🖨️ PDF Generation")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        create_pdf_button = st.button("Create PDF", type="primary", use_container_width=True)
    
    with col2:
        output_filename = st.text_input(
            "Output Filename", 
            value=f"MOC_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            placeholder="Enter PDF filename"
        )
    
    # Process the report when button is clicked
    if create_pdf_button:
        if not report_text.strip():
            st.error("❌ Please enter some report text first.")
        elif not output_filename.strip():
            st.error("❌ Please enter a filename for the PDF.")
        else:
            try:
                with st.spinner("📊 Parsing report data..."):
                    # Use ParsedReport to parse the text
                    parsed_report = ParsedReport(report_text)
                    
                    # Get the parsed data
                    windows = parsed_report.get_window_data()
                    offers_bids = parsed_report.get_offers_bids()
                    raw_trades = parsed_report.get_trades()
                    overviews = parsed_report.get_overviews()
                    
                    # let ai look at the raw_trades 
                    trades_ai = []
                    for trade in raw_trades:
                        trades_ai.extend(extract_trades_from_rawtext(trade, date = parsed_report.date))
                        
                        
                
                # Display parsing results
                st.success("✅ Report parsed successfully!")
                
                # Show summary of parsed data
                with st.expander("📋 Parsing Summary", expanded=False):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Windows", len(windows))
                    with col2:
                        st.metric("Offers/Bids", len(offers_bids))
                    with col3:
                        st.metric("Raw Trades", len(trades_ai))
                    with col4:
                        st.metric("Overviews", len(overviews))
                
                with st.spinner("🖨️ Generating PDF..."):
                    # Ensure output directory exists
                    output_dir = "output"
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # Full path for the output file
                    output_path = os.path.join(output_dir, output_filename)
                    if not output_filename.endswith('.pdf'):
                        output_path += '.pdf'

                    
                    # Create the PDF
                    create_trade_report_pdf(
                        file_path=output_path,
                        date=parsed_report.date,
                        trades=trades_ai,  # Empty for now - you may need to parse raw trades
                        overviews=overviews,
                        windows=windows,
                        offers_bids=offers_bids
                    )
                
                st.success(f"✅ PDF created successfully: `{output_path}`")
                
                # Provide download link if file exists
                if os.path.exists(output_path):
                    with open(output_path, "rb") as pdf_file:
                        pdf_bytes = pdf_file.read()
                        st.download_button(
                            label="📥 Download PDF",
                            data=pdf_bytes,
                            file_name=os.path.basename(output_path),
                            mime="application/pdf",
                            use_container_width=True
                        )
                
            except Exception as e:
                st.error(f"❌ Error processing report: {str(e)}")
                st.exception(e)  # Show full traceback for debugging
    
    # Information section
    st.divider()
    st.subheader("ℹ️ Instructions")
    
    with st.expander("📖 How to use", expanded=False):
        st.markdown("""
        **Steps to generate a MOC Report PDF:**
        
        1. **Login**: Make sure you're logged in using the Login tab
        2. **Paste Text**: Copy and paste your MOC report text into the text area above
        3. **Set Filename**: Enter a name for your PDF file (optional)
        4. **Create PDF**: Click the "Create PDF" button to process and generate the PDF
        5. **Download**: Use the download button to save the PDF to your computer
        
        **Expected Text Format:**
        - Date line at the top
        - Window dates section
        - Product sections separated by equal signs (====)
        - Each product should have Offers, Bids, Trades, and summary data
        """)
    
    with st.expander("🔧 Technical Details", expanded=False):
        st.markdown("""
        **Processing Pipeline:**
        1. Text input is processed by `ParsedReport` class
        2. Data is extracted into structured objects:
           - Windows: Delivery window information
           - Offers/Bids: Market participant data
           - Raw Trades: Trade text data
           - Overviews: Summary statistics
        3. PDF is generated using the `PdfCreation.py` module
        4. File is saved to the `output/` directory
        """)


def main():
    print("Starting MOC Report Streamlit App...")
    st.set_page_config(page_title="MOC Report", layout="wide")
    tab1, tab2 = st.tabs(["Login", "MOC Report"])
    with tab1:
        show_login_tab()
    with tab2:
        show_moc_report_tab()


if __name__ == "__main__":
    main()