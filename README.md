# CHURP TOPA Data Pipeline

Welcome to the CHURP TOPA Data Pipeline! This repository contains a series of tools designed to automatically download, clean, and enrich housing data from the DC Department of Housing and Community Development (DHCD). 

This guide is written for non-technical users to help you understand what each file does and how the overall process works.

---

## 📂 What does each file do?

The files in this folder are organized into sequential "steps" that take you from raw PDF reports all the way to a fully enriched dataset with coordinates and census data.

### Quick file reference
- `README.md`: Project guide and instructions for running the full pipeline.
- `step1a_extract_pdf_basic.py`: Downloads and parses newer DHCD TOPA PDFs into structured spreadsheet data.
- `step1b_extract_pdf_advanced.py`: Downloads and parses older TOPA PDFs with multiple legacy formats.
- `step2_reorganize_data.py`: Reshapes event-level records so each property address appears in a single row with timeline columns.
- `step3_separate_sfd_addresses.py`: Splits organized output into single-family and non-single-family property files.
- `geocode.py`: Uses Google Maps geocoding to add latitude and longitude for each address.
- `add_census_tract.py`: Uses Census APIs to add the census tract identifier from geographic coordinates.
- `add_census_data.ipynb`: Merges TOPA records with census demographic indicators.
- `add_median_rent.ipynb`: Adds neighborhood-level median rent data.
- `add_ward_blockgrp_age.ipynb`: Adds ward, block group, and housing age-related enrichment fields.
- `data.ipynb`: Notebook for exploratory analysis and validation of combined outputs.

### Step 1: Data Extraction (PDF to Excel)
These scripts go to the DHCD website, download the weekly TOPA (Tenant Opportunity to Purchase Act) PDF reports, and convert the text inside those PDFs into clean Excel spreadsheets.
* **`step1a_extract_pdf_basic.py`**: Handles newer reports (from 2024 to 2025). 
* **`step1b_extract_pdf_advanced.py`**: Handles older reports (from 2015 to 2023) because the DHCD used different formatting in the past (like the "2016" and "2021" formats). It automatically detects the format and extracts the data accordingly.

### Step 2: Data Organization
* **`step2_reorganize_data.py`**: The data pulled from the PDFs lists every single housing event as a new row. This script groups the data by address. It changes the layout so that each address gets exactly **one row**, and its entire history of events stretches out across columns (e.g., Date 1, Action 1, Date 2, Action 2).

### Step 3: Filtering
* **`step3_separate_sfd_addresses.py`**: This script looks at the organized data and separates the addresses into two distinct Excel files: one for Single Family Dwellings (SFD) and one for Non-SFD properties.

### Step 4: Geographic Enrichment (Mapping)
* **`geocode.py`**: This script takes your list of addresses and connects to the **Google Maps API**. It figures out the exact Latitude and Longitude for each address so they can be mapped out later.
* **`add_census_tract.py`**: Once the addresses are mapped, this script connects to the **US Census Bureau API** to find the 11-digit "Census Tract" ID for each property. 

### Step 5: Demographic Enrichment (Data Notebooks)
Finally, there are several Jupyter Notebook files (`.ipynb`). These are interactive data files that merge our housing data with external neighborhood statistics.
* **`add_census_data.ipynb`**: Merges the housing data with general census data.
* **`add_median_rent.ipynb`**: Adds median rent statistics for the neighborhoods.
* **`add_ward_blockgrp_age.ipynb`**: Adds details about the DC Ward, block groups, and building ages.
* **`data.ipynb`**: A general data exploration notebook.

---

## 🛠️ How to use this repository

To use these scripts, you will first need to download them to your computer.

### Step 0: Download the Project
There are two ways to download these files:

**Option 1: Download as a ZIP file (Easiest)**
1. Go to the GitHub page for this project.
2. Click the green **Code** button near the top right.
3. Select **Download ZIP**.
4. Once downloaded, double-click the ZIP file to extract it, and move the extracted folder to your Desktop.

**Option 2: Using the Terminal (Advanced)**
Open your Terminal (Mac) or Command Prompt (Windows) and run the following commands to clone the repository to your Desktop:
```bash
cd Desktop
git clone https://github.com/manojnathyogi/churptopa.git
```

### Prerequisites
You need Python installed on your computer. You also need to install the required "libraries" (helper tools) that these scripts rely on.
Open your Terminal (Mac) or Command Prompt (Windows) and run:
```bash
pip install pandas numpy requests beautifulsoup4 pdfplumber openpyxl
```

### Running the Steps
In your Terminal, navigate to this folder (`cd Desktop/churptopa`) and run the scripts one by one by typing `python` followed by the script name. 

For example, to start the first extraction:
```bash
python step1a_extract_pdf_basic.py
```
Wait for it to finish downloading and creating the Excel file, then move on to the next step:
```bash
python step2_reorganize_data.py
```

*Note: For the Google Maps Geocoder (`geocode.py`), you will need to open the file in a text editor and ensure your Google Maps API key is placed at the top where it says `API_KEY` before running it.*