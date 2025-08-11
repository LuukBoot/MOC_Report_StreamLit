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
        self.cell(40, 8, "Buyer", 1, 0, "C", True)
        self.cell(40, 8, "Seller", 1, 0, "C", True)
        self.cell(30, 8, "Window", 1, 0, "C", True)
        self.ln()
        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 11)
        for idx, t in enumerate(trades, start=1):
            self.cell(20, 6, str(idx), 1, 0, "C")
            self.cell(30, 6, f"${t.price:.2f}" if t.price is not None else "-", 1, 0, "C")
            self.cell(30, 6, f"{t.volume_kt:.2f}" if t.volume_kt is not None else "-", 1, 0, "C")
            self.cell(40, 6, t.buyer or "-", 1, 0, "C")
            self.cell(40, 6, t.seller or "-", 1, 0, "C")
            self.cell(30, 6, t.window or "-", 1, 0, "C")
            self.ln()
        self.ln(3)

    def add_overview_section(self, product_name: str, overview: OverView, offers: List[str], bids: List[str]):
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
        rows = [
            ("Offers", ', '.join(offers) if offers else "-"),
            ("Bids", ', '.join(bids) if bids else "-"),
            ("Average Price", f"${overview.avg_price:.2f}" if overview.avg_price is not None else "-"),
            ("Total Volume", f"{overview.total_volume:.2f} kt" if overview.total_volume is not None else "-"),
            ("Total Volume This Week", f"{overview.week_volume:.2f} kt" if overview.week_volume is not None else "-"),
            ("All Volume Up Till Now", f"{overview.cum_volume:.2f} kt" if overview.cum_volume is not None else "-"),
            ("Cumulative Average Price", f"${overview.cum_avg_price:.2f}" if overview.cum_avg_price is not None else "-"),
        ]
        for what, value in rows:
            self.cell(50, 9, what, 1, 0, "L")  # Thicker row: height 9
            x = self.get_x()
            y = self.get_y()
            self.multi_cell(140, 9, value, border=1, align="L")
            self.set_xy(x + 140, y)
            self.ln()
        self.ln(3)


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
    for product_name in products:
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
