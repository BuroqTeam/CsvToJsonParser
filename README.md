# CsvToJsonParser 
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
2. Create all necessary columns in the doc and fill in the data. Check [this](https://docs.google.com/spreadsheets/d/1Wr1iefSVw9_zGCJZGf6hYY06SQ01o4nH9DULol88fCA/edit?usp=sharing) link for the latest Sample SCV.
3. Download the doc as a `.csv` file and save it somewhere.
## Running The Project
```bash
# Print Help
python parser.py -h

# Parse CSV and Generate JSON
python parser.py --csv <CSV PATH> --outJson <JSON PATH>
# Provide only the CSV Filename. Output JSON Filename will be generated automatically
python parser.py --csv <CSV PATH> 
```