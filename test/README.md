# Test Folder for MOC Report PDF Generation

This test folder allows you to test the PDF generation functionality without running the Streamlit application every time you make changes to the code.

## Folder Structure

```
test/
├── input/          # Place your sample MOC report text files here
│   ├── sample_report_1.txt
│   ├── sample_report_2.txt
│   └── sample_report_3.txt
├── output/         # Generated PDF files will be saved here
├── test.py         # Main test script
└── README.md       # This file
```

## How to Use

### 1. Process All Files

Run the test script without arguments to process all `.txt` files in the input folder:

```bash
cd test
python test.py
```

This will:

- Find all `.txt` files in the `input/` folder
- Process each file through the same pipeline as the Streamlit app
- Generate PDF files in the `output/` folder
- Show a summary of successful and failed processing

### 2. Process a Specific File

Run the test script with a filename to process only that file:

```bash
cd test
python test.py sample_report_1.txt
```

### 3. Add Your Own Test Data

1. Create a new `.txt` file in the `input/` folder
2. Follow the MOC report format (see examples in existing sample files)
3. Run the test script to generate the PDF

## Expected Input Format

The input text files should follow this format:

```
Date: YYYY-MM-DD

Window dates:
FE  DD-DD Mon
MW  DD-DD Mon
BE  DD-DD Mon

===============================
ULSD 10ppm barges:

Offers: Company1/Company2
Bids: Company3/Company4

Trades:
Company1 sold X.Xkt to Company3 at $XXX.XX for FE window
Company2 sold X.Xkt to Company4 at $XXX.XX for MW window

Average Price: $XXX.XX
Total Volume: XX.X
Total volume this week: XX.X
All volume up till now: XX.X

===============================
50ppm barges:

Offers: Company5
Bids: Company6/Company7

Trades:
Company5 sold X.Xkt to Company6 at $XXX.XX for FE window

Average Price: $XXX.XX
Total Volume: XX.X
Total volume this week: XX.X
All volume up till now: XX.X
```

## What the Script Does

The test script replicates the exact same functionality as the Streamlit app button:

1. **Read Input**: Reads the text file from the input folder
2. **Parse Report**: Uses `ParsedReport` to extract structured data
3. **AI Processing**: Uses `extract_trades_from_rawtext` to process raw trade data
4. **Generate PDF**: Uses `create_trade_report_pdf` to create the final PDF
5. **Save Output**: Saves the PDF with a timestamp in the output folder

## Output Files

Generated PDF files are named with the pattern:
`{original_filename}_{timestamp}.pdf`

For example:

- `sample_report_1_20240821_143022.pdf`
- `sample_report_2_20240821_143025.pdf`

## Troubleshooting

### Import Errors

If you get import errors, make sure you're running the script from the `test/` directory:

```bash
cd test
python test.py
```

### No Files Found

If you get "No .txt files found", make sure you have `.txt` files in the `input/` folder.

### Processing Errors

Check the console output for detailed error messages. The script will show:

- Parsing results (number of windows, trades, etc.)
- AI processing progress
- Any errors that occur during processing

## Benefits of Using the Test Script

1. **Faster Development**: No need to start Streamlit every time
2. **Batch Processing**: Test multiple files at once
3. **Debugging**: See detailed console output and error messages
4. **Reproducible**: Same input will produce the same output
5. **Version Control**: Sample data files can be committed to git
