#!/usr/bin/env python3
"""
Test script for MOC Report PDF generation without Streamlit.

This script allows you to test the PDF generation functionality directly
by reading sample text files from the input folder and generating PDFs
in the output folder.

Usage:
    python test.py                          # Process all files in input folder
    python test.py sample_report_1.txt      # Process specific file
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add the parent directory and src directory to the path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
src_dir = parent_dir / 'src'
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(src_dir))

try:
    from src.ReportParser import ParsedReport
    from src.PdfCreation import create_trade_report_pdf
    from src.OpenAi import extract_trades_from_rawtext
    print("✅ All required modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure the src directory is properly configured.")
    sys.exit(1)


def process_report_file(input_file_path, output_dir):
    """
    Process a single report file and generate a PDF.
    
    Args:
        input_file_path (str): Path to the input text file
        output_dir (str): Directory to save the output PDF
    """
    print(f"\n📄 Processing: {input_file_path}")
    
    # Read the input file
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            report_text = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    if not report_text.strip():
        print("❌ File is empty or contains only whitespace")
        return False
    
    try:
        # Parse the report using ParsedReport
        print("📊 Parsing report data...")
        parsed_report = ParsedReport(report_text)
        
        # Get the parsed data
        windows = parsed_report.get_window_data()
        offers_bids = parsed_report.get_offers_bids()
        raw_trades = parsed_report.get_trades()
        overviews = parsed_report.get_overviews()
        
        print(f"  - Windows: {len(windows)}")
        print(f"  - Offers/Bids: {len(offers_bids)}")
        print(f"  - Raw Trades: {len(raw_trades)}")
        print(f"  - Overviews: {len(overviews)}")
        
        # Process raw trades with AI
        print("🤖 Processing trades with AI...")
        trades_ai = []
        for trade in raw_trades:
            ai_trades = extract_trades_from_rawtext(trade, date=parsed_report.date)
            trades_ai.extend(ai_trades)
            print(f"  - Processed {len(ai_trades)} trades from raw text")
        
        print(f"  - Total AI-processed trades: {len(trades_ai)}")
        
        # Generate output filename
        input_filename = Path(input_file_path).stem
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"{input_filename}_{timestamp}.pdf"
        output_path = os.path.join(output_dir, output_filename)
        
        # Create the PDF
        print("🖨️ Generating PDF...")
        create_trade_report_pdf(
            file_path=output_path,
            date=parsed_report.date,
            trades=trades_ai,
            overviews=overviews,
            windows=windows,
            offers_bids=offers_bids
        )
        
        print(f"✅ PDF created successfully: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing report: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """
    Main function to process report files.
    """
    print("🚀 MOC Report PDF Generator Test Script")
    print("=" * 50)
    
    # Setup directories
    current_dir = Path(__file__).parent
    input_dir = current_dir / 'input'
    output_dir = current_dir / 'output'
    
    # Ensure directories exist
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    print(f"📁 Input directory: {input_dir}")
    print(f"📁 Output directory: {output_dir}")
    
    # Check if specific file is requested
    if len(sys.argv) > 1:
        # Process specific file
        filename = sys.argv[1]
        input_file_path = input_dir / filename
        
        if not input_file_path.exists():
            print(f"❌ File not found: {input_file_path}")
            print(f"Available files in {input_dir}:")
            for f in input_dir.glob('*.txt'):
                print(f"  - {f.name}")
            return
        
        success = process_report_file(str(input_file_path), str(output_dir))
        if success:
            print("\n🎉 Processing completed successfully!")
        else:
            print("\n❌ Processing failed!")
    else:
        # Process all .txt files in input directory
        txt_files = list(input_dir.glob('*.txt'))
        
        if not txt_files:
            print(f"❌ No .txt files found in {input_dir}")
            print("Please add some sample report files to the input directory.")
            return
        
        print(f"📋 Found {len(txt_files)} files to process:")
        for f in txt_files:
            print(f"  - {f.name}")
        
        successful = 0
        failed = 0
        
        for txt_file in txt_files:
            success = process_report_file(str(txt_file), str(output_dir))
            if success:
                successful += 1
            else:
                failed += 1
        
        print(f"\n📊 Processing Summary:")
        print(f"  ✅ Successful: {successful}")
        print(f"  ❌ Failed: {failed}")
        print(f"  📁 Output files saved to: {output_dir}")


if __name__ == "__main__":
    main()
