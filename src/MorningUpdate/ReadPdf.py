import pandas as pd
import pdfplumber
import re

from src.OpenAi import summarize_pdf_text

class PjkGasoilExtractor:
    
    # standard info 
    page_num_table = 0
    line_text_start_data_rhine = "Duisburg [€/mton]"
    line_text_end_data_rhine = "Basle [€/mton]"
    line_text_start_data_ara = "ARA CROSS HARBOR"
    line_text_end_data_ara = "GHENT AMSTERDAM"
    
    # info based on the report type 
    type_report : str = "Rhine"  # or "ARA"

    
    # other types
    raw_text_first_page : str = ""
    
    # data_text
    data_text : list[str]
    
    # pandas dataframe of extracted tables
    df : pd.DataFrame = pd.DataFrame(columns=['location', 'avg price'])
    
    # summary text
    summary_text : str = ""
    
    
    
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        
        # get the raw text of the first page 
        with pdfplumber.open(self.pdf_path) as pdf:
            first_page = pdf.pages[0]
            self.raw_text_first_page = first_page.extract_text()
            




    def print_data_text(self):
        """Extract raw text from PDF, page by page.
        
        Returns:
            list: List of tuples containing (page_number, raw_text)
        """
        for line in self.data_text:
            print(line)


    def set_data_text(self):
        
        """Find the line that starts with 'Gasoil rate (av)' and return the line number where data starts.
                
        Returns:
            int: Line number where data starts (line after the header lines)
        """
        # find on the first page wher the line start with the text
        lines = self.raw_text_first_page.split('\n')
        self.data_text = []
        
        for i, line in enumerate(lines):
            
            # check if the line start wiht the rhine star text
            if line.startswith(self.line_text_start_data_rhine):
                self.type_report = "Rhine"

                # Start collecting data from the next line
                for j in range(i, len(lines)):
                    
                    # make sure if the line has CHF in it, we skip it
                    if "CHF" in lines[j]:
                        continue
                    self.data_text.append(lines[j])
                    if lines[j].startswith(self.line_text_end_data_rhine):
                        break
                break
                
            if line.startswith(self.line_text_start_data_ara):
                self.type_report = "ARA"

                # Start collecting data from the next line
                for j in range(i, len(lines)):
                    self.data_text.append(lines[j])
                    if lines[j].startswith(self.line_text_end_data_ara):
                        break
                break
        
        if not self.data_text:
            raise ValueError("Could not find the start of data in the PDF. Please check the report format.")

    def set_df(self):
        

        for line in self.data_text:
            # the price is the first number in the line 
            # Extract the first number from the line using regex
            match = re.search(r"([\d,]+\.?\d*)", line)
            # Extract location (text before the euro sign)
            euro_match = re.search(r"(.+?)\s*€", line)
            location = euro_match.group(1).strip() if euro_match else line.split()[0]
            # Remove brackets and their contents, then clean up extra spaces
            location = re.sub(r'\[.*?\]', '', location).strip()
            # Remove any remaining opening brackets
            location = re.sub(r'\[', '', location).strip()
            if match:
                avg_price = float(match.group(1).replace(',', ''))
                self.df = pd.concat([self.df, pd.DataFrame({'location': [location], 'avg price': [avg_price]})], ignore_index=True)
            else:
                raise ValueError(f"Could not extract location from line: {line}")

    def add_price_ranges(self, lower_variance: float = 0.1, upper_variance: float = 0.1):
        """Add price range columns to the dataframe.
        
        Args:
            lower_variance (float): Amount to subtract from avg price for minimum.
            upper_variance (float): Amount to add to avg price for maximum.
        """
        self.df['min price'] = self.df['avg price'] - lower_variance
        self.df['max price'] = self.df['avg price'] + upper_variance
        
        # add an column that will be displayed in the column on the pdf 
        self.df['price range'] = self.df.apply(lambda row: f"EUR {row['min price']:.2f} - {row['max price']:.2f}", axis=1)
    
    def set_summary_text(self):
        """Set the summary text using OpenAI to summarize the raw text of the first page."""
        self.summary_text = summarize_pdf_text(self.raw_text_first_page)       
       

        
        

        
        



# --- Example usage ---
if __name__ == "__main__":
    extractor = PjkGasoilExtractor("pjk_rhine_2025.08.01.pdf")
    extractor.extract_routes()
    df = extractor.to_dataframe()
    print(df)

