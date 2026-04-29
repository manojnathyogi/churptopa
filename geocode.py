import csv
import time
import requests
import sys

# === CONFIGURATION ===
# Replace this with your actual Google Maps API key
API_KEY = "AIzaSyBLtN1n_gyA7EUnqCDg_BFWYBWhRcylh4M"

# Input and output file names
INPUT_CSV = "final_merged_5p_remove2-4.csv"
OUTPUT_CSV = "final_merged_5_geocoded.csv"

# The name of the column in your CSV that contains the address. 
# You can change this if your column has a different header (e.g. 'Full Address')
ADDRESS_COLUMN = "Address"
# =====================

def geocode_address(address, api_key):
    """
    Geocodes an address using the Google Maps Geocoding API.
    """
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    params = {
        "address": address,
        "key": api_key
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() 
        
        data = response.json()
        
        if data['status'] == 'OK':
            results = data['results']
            if results:
                location = results[0]['geometry']['location']
                formatted_address = results[0]['formatted_address']
                
                return {
                    'lat': location['lat'],
                    'lng': location['lng'],
                    'formatted_address': formatted_address,
                    'status': 'OK'
                }
        else:
            error_msg = data.get('error_message', '')
            print(f"Error for address '{address}': {data['status']} - {error_msg}")
            return {
                'lat': '',
                'lng': '',
                'formatted_address': '',
                'status': data['status']
            }
            
    except requests.exceptions.RequestException as e:
        print(f"Request error for address '{address}': {e}")
        return {
            'lat': '',
            'lng': '',
            'formatted_address': '',
            'status': 'REQUEST_ERROR'
        }

def process_csv():
    if API_KEY == "YOUR_API_KEY_HERE":
        print("Error: Please replace 'YOUR_API_KEY_HERE' with your actual Google Maps API key at the top of the script.")
        sys.exit(1)
        
    try:
        with open(INPUT_CSV, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            
            # Check if the address column exists
            if ADDRESS_COLUMN not in reader.fieldnames:
                print(f"Error: Could not find column '{ADDRESS_COLUMN}' in {INPUT_CSV}.")
                print(f"Available columns are: {', '.join(reader.fieldnames)}")
                sys.exit(1)
                
            # Create a new list for output fieldnames
            output_fieldnames = reader.fieldnames + ['Latitude', 'Longitude', 'Formatted Address', 'Geocode Status']
            
            rows = list(reader)
            total_rows = len(rows)
            print(f"Found {total_rows} addresses to geocode. Starting process...")
            
            with open(OUTPUT_CSV, mode='w', encoding='utf-8', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=output_fieldnames)
                writer.writeheader()
                
                for i, row in enumerate(rows, 1):
                    address = row.get(ADDRESS_COLUMN, "")
                    
                    if address.strip():
                        print(f"[{i}/{total_rows}] Geocoding: {address}")
                        result = geocode_address(address, API_KEY)
                        
                        row['Latitude'] = result['lat']
                        row['Longitude'] = result['lng']
                        row['Formatted Address'] = result['formatted_address']
                        row['Geocode Status'] = result['status']
                        
                        # Add a small delay to avoid hitting Google Maps API rate limits (50 requests/second)
                        time.sleep(0.1)
                    else:
                        print(f"[{i}/{total_rows}] Skipping empty address row.")
                        row['Latitude'] = ''
                        row['Longitude'] = ''
                        row['Formatted Address'] = ''
                        row['Geocode Status'] = 'EMPTY_ADDRESS'
                        
                    writer.writerow(row)
                    
            print(f"\nSuccess! Finished geocoding. Results saved to '{OUTPUT_CSV}'.")
            
    except FileNotFoundError:
        print(f"Error: Could not find the file '{INPUT_CSV}'. Make sure it is in the same folder as this script.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    process_csv()
