#!/usr/bin/env python3
"""
Test script for MOC Report PDF generation with debugging capabilities.

This script allows you to test the PDF generation functionality directly
by reading sample text files from the input folder and generating PDFs
in the output folder. It also includes interactive debugging features.

Usage:
    python test.py                          # Interactive debug menu
    python test.py --process               # Process all files in input folder
    python test.py --file sample_report_1.txt    # Process specific file
    python test.py --debug                 # Debug mode for specific file
    python test.py --shell                 # Interactive Python shell
"""

import os
import sys
import pdb
import json
import traceback
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
    from src.models import Trade, Offers_Bids, Windows, OverView, RawTradeText
    print("✅ All required modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure the src directory is properly configured.")
    sys.exit(1)


class TestDebugger:
    """Interactive debugger for testing MOC Report logic"""
    
    def __init__(self):
        self.report_text = ""
        self.parsed_report = None
        self.sample_files = []
        self.debug_data = {}
        self._load_sample_files()
    
    def _load_sample_files(self):
        """Load available sample files"""
        input_dir = current_dir / 'input'
        if input_dir.exists():
            self.sample_files = list(input_dir.glob('*.txt'))
            print(f"📁 Found {len(self.sample_files)} sample files:")
            for i, file in enumerate(self.sample_files, 1):
                print(f"  {i}. {file.name}")
        else:
            print("⚠️ No input directory found")
    
    def load_file(self, filename: str = None) -> bool:
        """Load a report file for debugging"""
        if filename is None:
            if not self.sample_files:
                print("❌ No sample files available")
                return False
            
            print("\nSelect a file to debug:")
            for i, file in enumerate(self.sample_files, 1):
                print(f"  {i}. {file.name}")
            
            try:
                choice = int(input("Enter file number: ")) - 1
                if 0 <= choice < len(self.sample_files):
                    filename = self.sample_files[choice]
                else:
                    print("❌ Invalid choice")
                    return False
            except ValueError:
                print("❌ Invalid input")
                return False
        else:
            # Check if it's a full path or just filename
            file_path = Path(filename)
            if not file_path.exists():
                # Try in input directory
                file_path = current_dir / 'input' / filename
                if not file_path.exists():
                    print(f"❌ File not found: {filename}")
                    return False
            filename = file_path
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.report_text = f.read()
            print(f"✅ Loaded file: {filename}")
            print(f"📊 File size: {len(self.report_text)} characters")
            return True
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return False
    
    def parse_report(self, debug_mode: bool = False) -> bool:
        """Parse the loaded report with optional debugging"""
        if not self.report_text:
            print("❌ No report text loaded. Use load_file() first.")
            return False
        
        print("\n🔍 Starting report parsing...")
        
        if debug_mode:
            print("🐛 Debug mode: Setting breakpoint before parsing")
            pdb.set_trace()
        
        try:
            self.parsed_report = ParsedReport(self.report_text)
            self._store_debug_data()
            print("✅ Report parsed successfully!")
            self._print_parse_summary()
            return True
        except Exception as e:
            print(f"❌ Error parsing report: {e}")
            traceback.print_exc()
            return False
    
    def _store_debug_data(self):
        """Store parsed data for debugging"""
        if not self.parsed_report:
            return
        
        self.debug_data = {
            'date': self.parsed_report.date,
            'windows': [w.__dict__ for w in self.parsed_report.get_window_data()],
            'offers_bids': [ob.__dict__ for ob in self.parsed_report.get_offers_bids()],
            'raw_trades': [rt.__dict__ for rt in self.parsed_report.get_trades()],
            'overviews': [ov.__dict__ for ov in self.parsed_report.get_overviews()]
        }
    
    def _print_parse_summary(self):
        """Print summary of parsed data"""
        if not self.parsed_report:
            return
        
        windows = self.parsed_report.get_window_data()
        offers_bids = self.parsed_report.get_offers_bids()
        raw_trades = self.parsed_report.get_trades()
        overviews = self.parsed_report.get_overviews()
        
        print(f"\n📊 Parse Summary:")
        print(f"  📅 Date: {self.parsed_report.date}")
        print(f"  🪟 Windows: {len(windows)}")
        print(f"  💰 Offers/Bids: {len(offers_bids)}")
        print(f"  📈 Raw Trades: {len(raw_trades)}")
        print(f"  📋 Overviews: {len(overviews)}")
    
    def inspect_windows(self):
        """Inspect parsed windows data"""
        if not self.parsed_report:
            print("❌ No parsed report available")
            return
        
        windows = self.parsed_report.get_window_data()
        print(f"\n🪟 Windows Data ({len(windows)} items):")
        for i, window in enumerate(windows, 1):
            print(f"  {i}. Type: {window.type}, Dates: {window.Dates}")
    
    def inspect_offers_bids(self):
        """Inspect offers and bids data"""
        if not self.parsed_report:
            print("❌ No parsed report available")
            return
        
        offers_bids = self.parsed_report.get_offers_bids()
        print(f"\n💰 Offers/Bids Data ({len(offers_bids)} items):")
        
        for i, ob in enumerate(offers_bids, 1):
            print(f"  {i}. {ob.type.upper()}: {ob.product} - {ob.participant} @ {ob.price} ({ob.window})")
    
    def inspect_raw_trades(self):
        """Inspect raw trades data"""
        if not self.parsed_report:
            print("❌ No parsed report available")
            return
        
        raw_trades = self.parsed_report.get_trades()
        print(f"\n📈 Raw Trades Data ({len(raw_trades)} items):")
        
        for i, trade in enumerate(raw_trades, 1):
            print(f"  {i}. Product: {trade.product}")
            print(f"     Type: {trade.type}")
            print(f"     Text: {trade.text[:100]}...")
            print()
    
    def inspect_overviews(self):
        """Inspect overview data"""
        if not self.parsed_report:
            print("❌ No parsed report available")
            return
        
        overviews = self.parsed_report.get_overviews()
        print(f"\n📋 Overviews Data ({len(overviews)} items):")
        
        for i, overview in enumerate(overviews, 1):
            print(f"  {i}. Product: {overview.product}")
            print(f"     Day Avg: {overview.day_avg_price}")
            print(f"     Week Avg: {overview.week_avg_price}")
            print(f"     Cum Volume: {overview.cum_volume}")
            print(f"     Total Volume: {overview.total_volume}")
            print()
    
    def debug_ai_extraction(self, trade_index: int = None):
        """Debug AI trade extraction"""
        if not self.parsed_report:
            print("❌ No parsed report available")
            return
        
        raw_trades = self.parsed_report.get_trades()
        if not raw_trades:
            print("❌ No raw trades available")
            return
        
        if trade_index is None:
            print(f"Available raw trades (0-{len(raw_trades)-1}):")
            for i, trade in enumerate(raw_trades):
                print(f"  {i}. {trade.product} - {trade.type}")
            
            try:
                trade_index = int(input("Enter trade index to debug: "))
            except ValueError:
                print("❌ Invalid input")
                return
        
        if not (0 <= trade_index < len(raw_trades)):
            print(f"❌ Invalid trade index. Must be 0-{len(raw_trades)-1}")
            return
        
        trade = raw_trades[trade_index]
        print(f"\n🤖 Debugging AI extraction for trade {trade_index}:")
        print(f"Product: {trade.product}")
        print(f"Type: {trade.type}")
        print(f"Text: {trade.text}")
        print("\n🐛 Setting breakpoint before AI extraction...")
        
        pdb.set_trace()
        
        try:
            ai_trades = extract_trades_from_rawtext(trade, date=self.parsed_report.date)
            print(f"✅ AI extracted {len(ai_trades)} trades:")
            for i, ai_trade in enumerate(ai_trades, 1):
                print(f"  {i}. {ai_trade.buyer} -> {ai_trade.seller}: {ai_trade.volume_kt}kt @ {ai_trade.price}")
        except Exception as e:
            print(f"❌ AI extraction error: {e}")
            traceback.print_exc()
    
    def debug_pdf_generation(self):
        """Debug PDF generation"""
        if not self.parsed_report:
            print("❌ No parsed report available")
            return
        
        print("\n🖨️ Debugging PDF generation...")
        
        # First process all trades with AI
        print("🤖 Processing all trades with AI...")
        trades_ai = []
        raw_trades = self.parsed_report.get_trades()
        
        for i, trade in enumerate(raw_trades):
            print(f"  Processing trade {i+1}/{len(raw_trades)}: {trade.product}")
            try:
                ai_trades = extract_trades_from_rawtext(trade, date=self.parsed_report.date)
                trades_ai.extend(ai_trades)
                print(f"    ✅ Extracted {len(ai_trades)} trades")
            except Exception as e:
                print(f"    ❌ Error: {e}")
        
        print(f"📊 Total AI-processed trades: {len(trades_ai)}")
        
        # Setup output path
        output_dir = current_dir / 'output'
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = output_dir / f"debug_report_{timestamp}.pdf"
        
        print(f"📁 Output path: {output_path}")
        print("🐛 Setting breakpoint before PDF creation...")
        
        pdb.set_trace()
        
        try:
            create_trade_report_pdf(
                file_path=str(output_path),
                date=self.parsed_report.date,
                trades=trades_ai,
                overviews=self.parsed_report.get_overviews(),
                windows=self.parsed_report.get_window_data(),
                offers_bids=self.parsed_report.get_offers_bids()
            )
            print(f"✅ PDF created successfully: {output_path}")
        except Exception as e:
            print(f"❌ PDF generation error: {e}")
            traceback.print_exc()
    
    def export_debug_data(self, filename: str = None):
        """Export debug data to JSON"""
        if not self.debug_data:
            print("❌ No debug data available")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"debug_data_{timestamp}.json"
        
        output_path = current_dir / filename
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.debug_data, f, indent=2, default=str)
            print(f"✅ Debug data exported to: {output_path}")
        except Exception as e:
            print(f"❌ Export error: {e}")
    
    def interactive_shell(self):
        """Start interactive Python shell with all variables loaded"""
        import code
        
        # Prepare namespace
        namespace = {
            'debugger': self,
            'ParsedReport': ParsedReport,
            'create_trade_report_pdf': create_trade_report_pdf,
            'extract_trades_from_rawtext': extract_trades_from_rawtext,
            'Trade': Trade,
            'Offers_Bids': Offers_Bids,
            'Windows': Windows,
            'OverView': OverView,
            'RawTradeText': RawTradeText,
            'pdb': pdb,
            'current_dir': current_dir,
            'process_report_file': process_report_file,
        }
        
        if self.parsed_report:
            namespace.update({
                'parsed_report': self.parsed_report,
                'windows': self.parsed_report.get_window_data(),
                'offers_bids': self.parsed_report.get_offers_bids(),
                'raw_trades': self.parsed_report.get_trades(),
                'overviews': self.parsed_report.get_overviews(),
                'report_text': self.report_text,
            })
        
        print("\n🐍 Starting interactive Python shell...")
        print("Available variables:")
        for key in sorted(namespace.keys()):
            print(f"  - {key}")
        print("\nType 'help(debugger)' for debugger methods")
        print("Type 'exit()' to quit\n")
        
        code.interact(local=namespace, banner="")
    
    def run_interactive_menu(self):
        """Run interactive debugging menu"""
        while True:
            print("\n" + "="*50)
            print("🐛 MOC Report Test & Debug - Interactive Menu")
            print("="*50)
            print("1. Load report file")
            print("2. Parse report (normal)")
            print("3. Parse report (debug mode)")
            print("4. Inspect windows")
            print("5. Inspect offers/bids")
            print("6. Inspect raw trades")
            print("7. Inspect overviews")
            print("8. Debug AI extraction")
            print("9. Debug PDF generation")
            print("10. Export debug data")
            print("11. Interactive Python shell")
            print("12. Process all files (original functionality)")
            print("0. Exit")
            
            try:
                choice = input("\nEnter your choice (0-12): ").strip()
                
                if choice == '0':
                    print("👋 Goodbye!")
                    break
                elif choice == '1':
                    self.load_file()
                elif choice == '2':
                    self.parse_report(debug_mode=False)
                elif choice == '3':
                    self.parse_report(debug_mode=True)
                elif choice == '4':
                    self.inspect_windows()
                elif choice == '5':
                    self.inspect_offers_bids()
                elif choice == '6':
                    self.inspect_raw_trades()
                elif choice == '7':
                    self.inspect_overviews()
                elif choice == '8':
                    self.debug_ai_extraction()
                elif choice == '9':
                    self.debug_pdf_generation()
                elif choice == '10':
                    self.export_debug_data()
                elif choice == '11':
                    self.interactive_shell()
                elif choice == '12':
                    process_all_files()
                else:
                    print("❌ Invalid choice")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                traceback.print_exc()


def process_all_files():
    """Process all .txt files in input directory (original functionality)"""
    print("🚀 Processing all files in input directory...")
    
    # Setup directories
    input_dir = current_dir / 'input'
    output_dir = current_dir / 'output'
    
    # Ensure directories exist
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    print(f"📁 Input directory: {input_dir}")
    print(f"📁 Output directory: {output_dir}")
    
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


def process_report_file(input_file_path, output_dir, debug_mode=False):
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
        
        if debug_mode:
            print("🐛 Debug mode: Setting breakpoint before parsing")
            pdb.set_trace()
        
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
            if debug_mode:
                print(f"🐛 Debug mode: Processing trade - {trade.product}")
                pdb.set_trace()
            
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
        
        if debug_mode:
            print("🐛 Debug mode: Setting breakpoint before PDF creation")
            pdb.set_trace()
        
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
    Main function with enhanced debugging capabilities.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='MOC Report Test & Debug Tool')
    parser.add_argument('--process', action='store_true', help='Process all files in input folder')
    parser.add_argument('--file', '-f', help='Process specific file')
    parser.add_argument('--debug', '-d', action='store_true', help='Enable debug mode with breakpoints')
    parser.add_argument('--shell', '-s', action='store_true', help='Start interactive shell')
    
    args = parser.parse_args()
    
    # If no arguments provided, show interactive menu
    if not any([args.process, args.file, args.shell]):
        debugger = TestDebugger()
        debugger.run_interactive_menu()
        return
    
    # Handle command line arguments
    if args.shell:
        debugger = TestDebugger()
        debugger.interactive_shell()
        return
    
    if args.file:
        # Process specific file
        input_dir = current_dir / 'input'
        output_dir = current_dir / 'output'
        
        # Ensure directories exist
        input_dir.mkdir(exist_ok=True)
        output_dir.mkdir(exist_ok=True)
        
        input_file_path = input_dir / args.file
        
        if not input_file_path.exists():
            print(f"❌ File not found: {input_file_path}")
            print(f"Available files in {input_dir}:")
            for f in input_dir.glob('*.txt'):
                print(f"  - {f.name}")
            return
        
        success = process_report_file(str(input_file_path), str(output_dir), debug_mode=args.debug)
        if success:
            print("\n🎉 Processing completed successfully!")
        else:
            print("\n❌ Processing failed!")
    
    elif args.process:
        # Process all files (original functionality)
        process_all_files()


if __name__ == "__main__":
    main()
