import os
import sys
import pdb
import json
import traceback
from datetime import datetime
from pathlib import Path

# update



# Add the parent directory and src directory to the path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
src_dir = parent_dir / 'src'
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(src_dir))

try:
    from src.MorningUpdate.ReadPdf import PjkGasoilExtractor
    from src.PdfCreation import TradeReportPDF
    print("✅ All required modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure the src directory is properly configured.")
    sys.exit(1)
    


#filePath = "C:\\github repos\\MOC_Report_StreamLit\\test\\InputMorningupdate\\pjk_ara_fr_2025_08_01.pdf"

def test_pdf_extraction():
    #! check the rhine pdfs in the folder
    folder_path = Path("C:/github repos/MOC_Report_StreamLit/test/InputMorningupdate/rhine")
    for pdf_file in folder_path.glob("*.pdf"):
        # Process each PDF file here
        extractor = PjkGasoilExtractor(str(pdf_file))
        extractor.set_data_text()
        if extractor.type_report != "Rhine":
            print(f"Unexpected report type for {pdf_file.name}: {extractor.type_report}")
            continue
            
        # print the extracted data text for verification
        for line in extractor.data_text:
            print(line)
            
        print(f"successfully processed: {pdf_file.name} ✅")

        


    #! check the ara pdfs in the folder 
    folder_path = Path("C:/github repos/MOC_Report_StreamLit/test/InputMorningupdate/ara")
    for pdf_file in folder_path.glob("*.pdf"):
        print(f"Processing: {pdf_file.name}")

        # Process each PDF file here
        extractor = PjkGasoilExtractor(str(pdf_file))
        extractor.set_data_text()
        if extractor.type_report != "ARA":
            print(f"Unexpected report type for {pdf_file.name}: {extractor.type_report}")
            continue
        
        # print the extracted data text for verification
        for line in extractor.data_text:
            print(line)
        
        print(f"successfully processed: {pdf_file.name} ✅")

def test_specific_pdf():
    #filePath = "C:\\github repos\\MOC_Report_StreamLit\\test\\InputMorningupdate\\ara\\pjk_ara_fr_2025_08_01.pdf"
    filePath = r"C:\github repos\MOC_Report_StreamLit\test\InputMorningupdate\rhine\pjk_rhine_2025.08.01.pdf"
    extractor = PjkGasoilExtractor(filePath)
    extractor.set_data_text()
    
    print(f"Report Type: {extractor.type_report}")
    extractor.set_df()
    extractor.add_price_ranges()
    print(extractor.df)

def test_output_pdf():
    
    filePath1 = r"C:\github repos\MOC_Report_StreamLit\test\InputMorningupdate\pjk_ara_fr_2025_08_01.pdf"
    filePath2 = r"C:\github repos\MOC_Report_StreamLit\test\InputMorningupdate\pjk_rhine_2025.09.25.pdf"
    
    extractor = PjkGasoilExtractor(filePath1)
    extractor.set_data_text()
    extractor.set_df()
    extractor.add_price_ranges()
    extractor.set_summary_text()
    
    extractor2 = PjkGasoilExtractor(filePath2)
    extractor2.set_data_text()
    extractor2.set_df()
    extractor2.add_price_ranges(lower_variance=0.1, upper_variance=0.2)
    extractor2.set_summary_text()
    
    
    

    
    pdf = TradeReportPDF(orientation="P", unit="mm", format="A4")
    pdf.report_date = "2025-08-01"
    
    # add two pages 
    pdf.add_page()
    
    # add the ara section
    if extractor.type_report == "ARA":
        pdf.add_ara_section(extractor)
    if extractor2.type_report == "ARA":
        pdf.add_ara_section(extractor2)
    pdf.add_page()
    if extractor.type_report == "Rhine":
        pdf.add_rhine_section(extractor)
    if extractor2.type_report == "Rhine":
        pdf.add_rhine_section(extractor2)

    
    
    
    # save the pdf
    output_path = r"C:\github repos\MOC_Report_StreamLit\test\output\test_report.pdf"
    pdf.output(output_path)
    
    
    