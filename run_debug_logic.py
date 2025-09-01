#!/usr/bin/env python3
"""
Simple debug script to run the MOC Report logic step by step.

This script loads a sample file and runs through the exact same logic
as the Streamlit app, allowing you to debug each step.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.insert(0, str(current_dir))
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


def run_debug_logic():
    """Run the same logic as the Streamlit app step by step"""
    
    # Load sample file
    input_dir = current_dir / 'test' / 'input'
    sample_file_name = "sample_report_6.txt"
    sample_file = input_dir / sample_file_name

    if not sample_file.exists():
        print(f"❌ File not found: {sample_file}")
        return

    print(f"📄 Loading file: {sample_file.name}")
    
    # Read the report text
    with open(sample_file, 'r', encoding='utf-8') as f:
        report_text = f.read()
    
    print(f"📊 File loaded: {len(report_text)} characters")
    print("=" * 50)
    
    # Step 1: Use ParsedReport to parse the text
    print("🔍 Step 1: Parsing report text...")
    parsed_report = ParsedReport(report_text)
    print(f"✅ Report parsed successfully!")
    print(f"📅 Date: {parsed_report.date}")
    print()
    
    # Step 2: Get the parsed data
    print("🔍 Step 2: Getting parsed data...")
    windows = parsed_report.get_window_data()
    offers_bids = parsed_report.get_offers_bids()
    raw_trades = parsed_report.get_trades()
    overviews = parsed_report.get_overviews()
    
    print(f"🪟 Windows: {len(windows)}")
    print(f"💰 Offers/Bids: {len(offers_bids)}")
    print(f"📈 Raw Trades: {len(raw_trades)}")
    print(f"📋 Overviews: {len(overviews)}")
    print()
    
    # Step 3: Let AI look at the raw_trades
    print("🔍 Step 3: Processing raw trades with AI...")
    trades_ai = []
    for i, trade in enumerate(raw_trades):
        print(f"  Processing trade {i+1}/{len(raw_trades)}: {trade.product}")
        ai_trades = extract_trades_from_rawtext(trade, date=parsed_report.date)
        trades_ai.extend(ai_trades)
        print(f"    ✅ Extracted {len(ai_trades)} AI trades")
    
    print(f"🤖 Total AI trades: {len(trades_ai)}")
    print()
    
    # Display results
    print("=" * 50)
    print("📊 FINAL RESULTS:")
    print("=" * 50)
    print(f"📅 Date: {parsed_report.date}")
    print(f"🪟 Windows: {len(windows)}")
    print(f"💰 Offers/Bids: {len(offers_bids)}")
    print(f"📈 Raw Trades: {len(raw_trades)}")
    print(f"🤖 AI Processed Trades: {len(trades_ai)}")
    print(f"📋 Overviews: {len(overviews)}")
    
    # Show some details
    if windows:
        print("\n🪟 Windows Details:")
        for i, window in enumerate(windows):
            print(f"  {i+1}. {window.type}: {window.Dates}")
    
    if offers_bids:
        print("\n💰 Offers/Bids Details:")
        for i, ob in enumerate(offers_bids[:5]):  # Show first 5
            print(f"  {i+1}. {ob.type}: {ob.product} - {ob.participant} @ {ob.price}")
        if len(offers_bids) > 5:
            print(f"  ... and {len(offers_bids) - 5} more")
    
    if trades_ai:
        print("\n🤖 AI Trades Details:")
        for i, trade in enumerate(trades_ai[:5]):  # Show first 5
            print(f"  {i+1}. {trade.buyer} -> {trade.seller}: {trade.volume_kt}kt @ {trade.price}")
        if len(trades_ai) > 5:
            print(f"  ... and {len(trades_ai) - 5} more")
    
    if overviews:
        print("\n📋 Overviews Details:")
        for i, overview in enumerate(overviews):
            print(f"  {i+1}. {overview.product}:")
            print(f"      Day Avg: {overview.day_avg_price}")
            print(f"      Week Avg: {overview.week_avg_price}")
            print(f"      Cum Volume: {overview.cum_volume}")
            
    # Step 4: Create PDF report
    print("\n🔍 Step 4: Creating PDF report...")
    try:
        output_dir = current_dir / 'test' / 'output'
        output_dir.mkdir(exist_ok=True)
        
        pdf_filename = f"moc_report_{parsed_report.date}.pdf"
        pdf_path = output_dir / pdf_filename
        file_path = pdf_path.resolve()
        
        create_trade_report_pdf(
            file_path=file_path,
            trades=trades_ai,
            offers_bids=offers_bids,
            windows=windows,
            overviews=overviews,
            date=parsed_report.date
        )
        
        print(f"✅ PDF created successfully: {pdf_path}")
        print(f"📄 PDF size: {pdf_path.stat().st_size} bytes")
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
    


if __name__ == "__main__":
    print("🚀 Running MOC Report Debug Logic")
    print("=" * 50)
    run_debug_logic()
