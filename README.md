# CsvToJsonParser
## About
This project helps with generating JSON Docs from CSV Docs.
## Prerequisites
* Python 3.10+
## Project Setup
1. Clone the Project:
   ```bash
   git clone git@github.com:BuroqTeam/CsvToJsonParser.git
   ```
2. Create and Activate Virtual Environment
   ```bash
   cd CsvToJsonParser/
   pip3 install virtualenv
   virtualenv -p python3 venv
   # Linux
   source venv/bin/activate
   # Windows
   venv\Scripts\activate.bat
   ```
3. Install Requirements
   ```bash
   pip install -r requirements.txt
   ```
## Preparing the Input Data
1. Create a Google Sheets Doc.
2. Create a sheet for each Question Pattern in the doc.
2. Create all necessary columns in the sheets and fill in the data. Check [this](https://docs.google.com/spreadsheets/d/1Wr1iefSVw9_zGCJZGf6hYY06SQ01o4nH9DULol88fCA/edit?usp=sharing) link for the latest template of the CSV.
3. Download the sheets as `.csv` files and save them into a folder.
## Running The Project
### Generating JSON from CSV
```bash
# Print Help
python csvToJsonParser.py -h

# Parse CSVs and Generate JSON
python csvToJsonParser.py --csv <FOLDER PATH WHERE CSV FILES ARE LOCATED> --grade <GRADE WHICH THE QUESTIONS BELONG TO> --language <LANGUAGE CODE> --subject <SUBJECT>
 # Example
python csvToJsonParser.py --csv C:\User\Downloads\CSV --grade 6 --language uz --subject math

# Adding --outJson <JSON PATH> will result in saving the generated JSON File in <JSON PATH> path
python csvToJsonParser.py --csv C:\User\Downloads\CSV --grade 6 --language uz --subject math --outJson C:\Output\math-grade-6-uz.json
```