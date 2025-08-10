# MOC Report Generator GUI

A Streamlit-based graphical user interface for generating PDF reports from MOC (Market-on-Close) trading data.

## Features

### 🔐 Login Tab

- Simple authentication system
- Session management
- User status display
- Demo credentials: `admin` / `password`

### 📊 MOC Report Tab

- Text input for raw MOC report data
- Automatic parsing using `ParsedReport` class
- PDF generation with professional formatting
- Download functionality for generated PDFs
- Real-time parsing summary

## Quick Start

### Option 1: Using the launcher (Recommended)

```bash
python run_gui.py
```

### Option 2: Direct Streamlit execution

```bash
streamlit run GUI/main.py
```

## Usage Instructions

1. **Start the Application**

   - Run `python run_gui.py` from the project root
   - The application will open in your default web browser

2. **Login** (Login Tab)

   - Use username: `admin` and password: `password`
   - Click "Login" to authenticate

3. **Generate Report** (MOC Report Tab)
   - Paste your MOC report text in the text area
   - Optionally modify the output filename
   - Click "Create PDF" to generate the report
   - Download the generated PDF using the download button

## Expected Input Format

The MOC report text should follow this structure:

```
Date: 2024-01-15

Window dates:
FE  15-16 Jan
MW  17-18 Jan
BE  19-20 Jan

===============================
ULSD 10ppm barges:

Offers: Company A/Company B
Bids: Company C/Company D

Trades:
Trade details here...

Average Price: $650.50
Total Volume: 25.0
Total volume this week: 15.0
All volume up till now: 40.0

===============================
50ppm barges:
...
```

## Technical Details

### Processing Pipeline

1. Raw text input is processed by the `ParsedReport` class
2. Data is extracted into structured objects:
   - **Windows**: Delivery window information
   - **Offers/Bids**: Market participant data
   - **Raw Trades**: Trade text data
   - **Overviews**: Summary statistics
3. PDF is generated using the `PdfCreation.py` module
4. File is saved to the `output/` directory

### File Structure

```
GUI/
├── main.py           # Main application entry point
├── LoginTab.py       # Login interface
└── MocRerportTab.py  # MOC report processing interface

src/
├── data_extractor.py # ParsedReport class
├── PdfCreation.py    # PDF generation logic
└── models.py         # Data models

run_gui.py            # Application launcher
```

## Dependencies

- `streamlit` - Web application framework
- `fpdf2` - PDF generation
- `numpy` - Numerical operations
- Standard Python libraries

## Troubleshooting

### Import Errors

If you see import errors, ensure:

- All dependencies are installed: `pip install -r requirements.txt`
- You're running from the project root directory
- The `src/` directory contains all required modules

### PDF Generation Issues

- Check that the `output/` directory exists (created automatically)
- Verify that the MOC report text follows the expected format
- Ensure you have write permissions in the project directory

## Development

The GUI is built using Streamlit with a modular tab-based architecture. Each tab is implemented as a separate module for easy maintenance and extension.

Key components:

- **Session Management**: Handles user authentication state
- **Error Handling**: Graceful handling of parsing and generation errors
- **Real-time Feedback**: Progress indicators and status updates
- **Download Integration**: Direct PDF download functionality
