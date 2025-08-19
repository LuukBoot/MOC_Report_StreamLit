from fpdf import FPDF
from typing import List, Optional
from dataclasses import dataclass
import os
from .models import Trade, Offers_Bids, Windows, OverView, RawTradeText



# === PDF Builder ===
class TradeReportPDF(FPDF):
    def header(self):
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Logo", "Logo_starfeuls.png")
        if os.path.exists(logo_path):
            self.image(logo_path, x=160, y=10, w=30)
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "Starfuels Report", ln=True, align="C")
        self.set_font("Helvetica", "", 12)
        self.cell(0, 8, f"MOC Summary {self.report_date}", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_windows_section(self, windows: List[Windows]):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 8, "Delivery Windows", ln=True)
        self.set_fill_color(34, 139, 34)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 11)
        self.cell(60, 8, "Window", 1, 0, "C", True)
        self.cell(80, 8, "Date", 1, 0, "C", True)
        self.ln()
        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 11)
        for w in windows:
            self.cell(60, 6, w.type or "-", 1, 0, "C")
            self.cell(80, 6, w.Dates or "-", 1, 0, "C")
            self.ln()
        self.ln(5)

    def add_trades_section(self, product_name: str, trades: List[Trade]):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 8, f"{product_name} - Trades", ln=True)
        self.set_fill_color(34, 139, 34)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 11)
        self.cell(20, 8, "#", 1, 0, "C", True)
        self.cell(30, 8, "Price", 1, 0, "C", True)
        self.cell(30, 8, "Volume", 1, 0, "C", True)
        self.cell(40, 8, "Seller", 1, 0, "C", True)  # Swapped
        self.cell(40, 8, "Buyer", 1, 0, "C", True)   # Swapped
        self.cell(30, 8, "Window", 1, 0, "C", True)
        self.ln()
        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 11)
        for idx, t in enumerate(trades, start=1):
            self.cell(20, 6, str(idx), 1, 0, "C")
            self.cell(30, 6, f"${t.price:.2f}" if t.price is not None else "-", 1, 0, "C")
            self.cell(30, 6, f"{t.volume_kt:.2f}" if t.volume_kt is not None else "-", 1, 0, "C")
            self.cell(40, 6, t.seller or "-", 1, 0, "C")  # Swapped
            self.cell(40, 6, t.buyer or "-", 1, 0, "C")   # Swapped
            self.cell(30, 6, t.window or "-", 1, 0, "C")
            self.ln()
        self.ln(3)

    def add_overview_section(self, product_name: str, overview: OverView, offers: List[str], bids: List[str]):
        self.set_font("Helvetica", "B", 14)
        
        # Prepare all rows first to calculate total height needed
        rows = [
            ("Offers", ', '.join(offers) if offers else "-"),
            ("Bids", ', '.join(bids) if bids else "-"),
            ("Average Price", f"${overview.day_avg_price:.2f}" if overview.day_avg_price is not None else "-"),
            ("Total Volume", f"{overview.total_volume:.2f} kt" if overview.total_volume is not None else "-"),
            ("Total Volume This Week", f"{overview.week_volume:.2f} kt" if overview.week_volume is not None else "-"),
            ("All Volume Up Till Now", f"{overview.cum_volume:.2f} kt" if overview.cum_volume is not None else "-"),
            ("Week Average Price", f"${overview.week_avg_price:.2f}" if overview.week_avg_price is not None else "-"),
        ]
        
        # Calculate total height needed for the entire table
        total_height = 8 + 8  # Title + header row height
        base_height = 9
        
        self.set_font("Helvetica", "", 11)  # Set font for width calculations
        for what, value in rows:
            # Calculate lines needed for this row
            lines_needed = 1
            if self.get_string_width(value) > 140:
                words = value.split()
                current_line = ""
                line_count = 1
                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    if self.get_string_width(test_line) > 140:
                        line_count += 1
                        current_line = word
                    else:
                        current_line = test_line
                lines_needed = line_count
            
            row_height = base_height * lines_needed
            total_height += row_height
        
        total_height += 3  # Bottom margin
        
        # Check if table fits on current page (leave 20mm margin from bottom)
        page_height = 297  # A4 height in mm
        bottom_margin = 20
        available_height = page_height - self.get_y() - bottom_margin
        
        if total_height > available_height:
            self.add_page()
        
        # Now draw the table
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 8, f"{product_name} - Overview", ln=True)
        self.set_fill_color(34, 139, 34)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 11)
        # Make "What" column 50mm, "Value" column 120mm (wider)
        self.cell(50, 8, "What", 1, 0, "C", True)
        self.cell(140, 8, "Value", 1, 0, "C", True)
        self.ln()
        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 11)
        
        for what, value in rows:
            # Calculate the number of lines needed for the value text
            lines_needed = self.get_string_width(value) // 140 + 1
            if lines_needed > 1:
                # Check more precisely by splitting the text
                words = value.split()
                current_line = ""
                line_count = 1
                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    if self.get_string_width(test_line) > 140:
                        line_count += 1
                        current_line = word
                    else:
                        current_line = test_line
                lines_needed = line_count
            
            # Calculate row height based on number of lines
            row_height = base_height * lines_needed
            
            # Store current position
            start_x = self.get_x()
            start_y = self.get_y()
            
            # Draw the "What" cell with calculated height and vertical centering
            self.cell(50, row_height, what, 1, 0, "L")
            
            # Move to value column position
            self.set_xy(start_x + 50, start_y)
            
            # For multi-line text, we need to manually center it vertically
            if lines_needed > 1:
                # Calculate vertical offset to center the text
                text_height = lines_needed * base_height
                vertical_offset = (row_height - text_height) / 2
                
                # Draw border first
                self.cell(140, row_height, "", 1, 0, "L")
                
                # Move to text position with vertical centering
                self.set_xy(start_x + 50 + 2, start_y + vertical_offset)  # +2 for left padding
                
                # Draw the multi-line text without border (since we already drew it)
                self.multi_cell(136, base_height, value, border=0, align="L")  # 136 = 140 - 4 for padding
            else:
                # Single line - use regular cell with vertical centering
                self.cell(140, row_height, value, 1, 0, "L")
            
            # Move to next row
            self.set_xy(start_x, start_y + row_height)
            
        self.ln(3)
from fpdf import FPDF

# === Main Function ===
def create_trade_report_pdf(file_path: str, date: str, trades: List[Trade], overviews: List[OverView], windows: List[Windows], offers_bids: List[Offers_Bids]):
    pdf = TradeReportPDF(orientation="P", unit="mm", format="A4")
    pdf.report_date = date
    pdf.add_page()

    # Windows section
    pdf.add_windows_section(windows)

    # Group trades by product
    products = sorted(set(t.product for t in trades))
    products = ["ULSD 10ppm barges", "50ppm barges"]
    print(f"Found products: {products}")
    for idx, product_name in enumerate(products):
        # Add a new page for the second product and beyond
        if idx > 0:
            pdf.add_page()
        
        product_trades = [t for t in trades if t.product == product_name]
        product_overview = next((o for o in overviews if o.product == product_name), None)
        offers = [ob.participant for ob in offers_bids if ob.product == product_name and ob.type == "offer"]
        bids = [ob.participant for ob in offers_bids if ob.product == product_name and ob.type == "bid"]

        # Trades table
        pdf.add_trades_section(product_name, product_trades)

        # Overview table
        if product_overview:
            pdf.add_overview_section(product_name, product_overview, offers, bids)

    pdf.output(file_path)
    print(f"PDF report saved to {file_path}")
