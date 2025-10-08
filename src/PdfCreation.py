from fpdf import FPDF
import os
from src.MorningUpdate.ReadPdf import GasOilExtractor



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

    def add_ara_section(self, araData :GasOilExtractor):
        df = araData.df
        
        # only add the columns location and price range
        df = df[['location', 'price range']]
        
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 8, "ARA Barge Freight Market - Gasoil Routes", ln=True)
        self.set_font("Helvetica", "", 12)
        self.ln(2)
        self.set_fill_color(34, 139, 34)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 11)
        self.cell(100, 8, "Location", 1, 0, "C", True)
        self.cell(90, 8, "Rate [EUR/ton]", 1, 0, "C", True)
        self.ln()
        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 11)
        for _, row in df.iterrows():
            self.cell(100, 6, row['location'], 1, 0, "C")
            self.cell(90, 6, row['price range'], 1, 0, "C")
            self.ln()
        
        self.ln(5)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 12, "Summary:", ln=True)
        self.set_font("Helvetica", "", 12)
        # Encode text to handle Unicode characters
        summary_text = araData.summary_text.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 6, summary_text)
        
    def add_rhine_section(self, rhineData :GasOilExtractor):
        df = rhineData.df
        
        # only add the columns location and price range
        df = df[['location', 'price range']]
        
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 8, "Rhine Barge Freight Market - Gasoil Destinations", ln=True)
        self.set_font("Helvetica", "", 12)
        self.ln(2)
        self.set_fill_color(34, 139, 34)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 11)
        self.cell(100, 8, "Location", 1, 0, "C", True)
        self.cell(90, 8, "Rate [EUR/ton]", 1, 0, "C", True)
        self.ln()
        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 11)
        for _, row in df.iterrows():
            self.cell(100, 6, row['location'], 1, 0, "C")
            self.cell(90, 6, row['price range'], 1, 0, "C")
            self.ln()
    
        self.ln(5)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 12, "Summary:", ln=True)
        self.set_font("Helvetica", "", 12)
        # Encode text to handle Unicode characters
        summary_text = rhineData.summary_text.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 6, summary_text)

    def add_rhine_water_levels(self, df):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 8, "Rhine Water Levels", ln=True)
        self.set_font("Helvetica", "", 12)
        self.ln(2)
        self.set_fill_color(34, 139, 34)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 11)
        self.cell(60, 8, "Location", 1, 0, "C", True)
        self.cell(60, 8, "Current Level [cm]", 1, 0, "C", True)
        self.cell(60, 8, "Change [cm]", 1, 0, "C", True)
        self.ln()
        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 11)
        for _, row in df.iterrows():
            self.cell(60, 6, row['Station'], 1, 0, "C")
            self.cell(60, 6, str(row['Current (cm)']), 1, 0, "C")
            self.cell(60, 6, str(row['4 day - Forecast (cm)']), 1, 0, "C")
            self.ln()
        self.ln(5)

