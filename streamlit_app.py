import os
import sys
import streamlit as st
from datetime import datetime
import pandas as pd

# Add the src directory to the path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

try:
    from src.ReportParser import ParsedReport
    from src.OpenAi import extract_trades_from_rawtext
    from MorningUpdate.ReadPdf import PjkGasoilExtractor
    from src.PdfCreation import TradeReportPDF
    import time
    import json
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please ensure the src directory is properly configured.")




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

def show_barging_update():
    """Display the Barging Update tab with information about barging updates."""
    
    st.header("🚢 Barging Update")
    
    st.subheader("📅 Latest Updates")
    # PDF Upload Section
    uploaded_files = st.file_uploader("Upload PDF Reports", type=['pdf'], accept_multiple_files=True)
        
    if len(uploaded_files) != 2:
        st.warning("⚠️ Please upload exactly 2 PDF files.")
    else:
        st.success("✅ Two PDF files uploaded successfully!")

    # Analysis Section
    if st.button("Analyse Files", type="primary", use_container_width=True):
        with st.spinner("Analyzing uploaded files..."):
            # Process both files
            extractor_files = []
            
            for i, uploaded_file in enumerate(uploaded_files, 1):
                # Save uploaded file temporarily
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                try:
                    # Initialize the extractor
                    extractor = PjkGasoilExtractor(temp_path)
                    extractor.set_data_text()
                    extractor.set_df()
                    extractor.add_price_ranges()
                    extractor.set_summary_text()
                    
                    extractor_files.append(extractor)
                    
                    # Clean up temp file
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                        
                except Exception as e:
                    st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
            
            # Store extractors in session state
            st.session_state['extractor_files'] = extractor_files
    
    
    
    # Display results if extractors exist in session state
    if 'extractor_files' in st.session_state:
        


        for extractor in st.session_state['extractor_files']:
            extractor : PjkGasoilExtractor
            if extractor.type_report == "ARA":
                extractorAra = extractor
            elif extractor.type_report == "Rhine":
                extractorRhine = extractor

        # Display ARA section
        if extractorAra:
            with st.expander("🏭 ARA Data", expanded=True):
                
                # ARA Variance inputs
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.number_input("Lower Variance:", key='lower_variance_ara', value=0.1)
                with col2:
                    st.number_input("Upper Variance:", key='upper_variance_ara', value=0.1)
                with col3:
                    if st.button("Update Price Ranges", key="update_ara_ranges", use_container_width=True):
                        extractorAra.add_price_ranges(
                            lower_variance=st.session_state.get('lower_variance_ara', 0.1),
                            upper_variance=st.session_state.get('upper_variance_ara', 0.1)
                        )
                        st.success("✅ Price ranges updated!")
                
                # ARA DataFrame
                show_df_ara = extractorAra.df[['location', 'avg price', 'price range']]
                st.dataframe(show_df_ara, use_container_width=True)
                
                # ARA Summary input
                st.text_area(
                    "ARA Summary:",
                    value=extractorAra.summary_text,
                    height=300,
                    placeholder="Enter ARA analysis summary...",
                    key='summary_ARA'
                )

        # Display Rhine section
        if extractorRhine:
            with st.expander("🚢 Rhine Data", expanded=True):
                # Rhine DataFrame
                col1, col2, col3 = st.columns([1,6,1])
                with col1:
                    st.number_input("Lower Variance:", key='lower_variance_rhine', value = 0.1)
                with col2:
                    st.number_input("Upper Variance:", key='upper_variance_rhine', value = 0.1)
                with col3:
                    if st.button("Update Price Ranges", use_container_width=True):
                        extractorRhine.add_price_ranges(
                            lower_variance=st.session_state.get('lower_variance_rhine', 0.1),
                            upper_variance=st.session_state.get('upper_variance_rhine', 0.1)
                        )
                        st.success("✅ Price ranges updated!")
                
                show_df_rhine = extractorRhine.df[['location', 'avg price', 'price range']]
                st.dataframe(show_df_rhine, use_container_width=True)

                # Rhine Summary input
                st.text_area(
                    "Rhine Summary:",
                    value= extractorRhine.summary_text,
                    height=300,
                    placeholder="Enter Rhine analysis summary...",
                    key='summary_Rhine'
                )
            
            with st.expander("🌊 Rhine Water Levels", expanded=True):
                
                # Rhine Water Levels Section
                st.subheader("🌊 Rhine Water Levels")

                # create an df
                df_rhine_levels = pd.DataFrame({
                    "Station": ["Ruhrort", "Cologne", "Kaub", "Maxau"],
                    "Current (cm)": [0, 0, 0, 0],
                    "4 day - Forecast (cm)": [0, 0, 0, 0]
                })
                
                # Editable Rhine water levels
                edited_df = st.data_editor(
                    df_rhine_levels,
                    use_container_width=True,
                    key="rhine_levels_editor"
                )
                
                # Store the edited Rhine water levels data
                st.session_state['rhine_water_levels'] = edited_df




    # Create PDF button
    if st.button(f"Create barging PDF Report"):
        # You can add PDF generation logic here
            pdf = TradeReportPDF(orientation="P", unit="mm", format="A4")
            pdf.report_date = datetime.now().strftime("%d-%m-%Y")
            
            # add two pages 
            pdf.add_page()
            
            # update the summary texts from the text areas
            if extractorAra:
                extractorAra.summary_text = st.session_state.get('summary_ARA', extractorAra.summary_text)
            if extractorRhine:
                extractorRhine.summary_text = st.session_state.get('summary_Rhine', extractorRhine.summary_text)
            
            # add the ara section
            if extractorAra:
                pdf.add_ara_section(extractorAra)
            pdf.add_page()
            if extractorRhine:
                pdf.add_rhine_section(extractorRhine)
                
            pdf.add_page()
            pdf.add_rhine_water_levels(st.session_state.get('rhine_water_levels', pd.DataFrame()))

    
    
            
            # save the pdf
            filename = f"barging_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            output_dir = os.path.join(os.path.dirname(__file__), "output")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, filename)
            pdf.output(output_path)
            
            # Provide download button for the PDF
            with open(output_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_file,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True
                )

            st.success("✅ PDF created successfully!")


def main():
    print("Starting MOC Report Streamlit App...")
    st.set_page_config(page_title="MOC Report", layout="wide")
    tab1, tab2 = st.tabs(["Login", "Barging Update"])
    with tab1:
        show_login_tab()
    with tab2:
        show_barging_update()



if __name__ == "__main__":
    main()