import pandas as pd
import numpy as np
from datetime import datetime

def reorganize_data(input_file, output_file, sheet_name='Sorted'):
    """
    Reorganize data from long format to wide format.
    Each address gets one row with multiple Date_X, Action_X, Units_X, Price_X columns.
    
    Parameters:
    -----------
    input_file : str
        Path to input Excel file
    output_file : str
        Path to output Excel file
    sheet_name : str
        Name of the sheet to process (default: 'Sorted')
    """
    
    print(f"Loading data from '{input_file}', sheet '{sheet_name}'...")
    df = pd.read_excel(input_file, sheet_name=sheet_name)
    
    print(f"Original data shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Rename columns for easier handling
    df.columns = ['Address', 'Date', 'Action', 'Units', 'Price']
    
    # Group by Address and get all records for each address
    print("\nGrouping by Address...")
    grouped = df.groupby('Address', sort=False)
    
    # Find maximum number of records for any address (to know how many columns we need)
    max_records = grouped.size().max()
    print(f"Maximum number of records for a single address: {max_records}")
    
    # Create the new dataframe structure
    result_data = []
    
    for address, group in grouped:
        # Sort the group by date if needed (optional - remove if you want to keep original order)
        # group = group.sort_values('Date')
        
        # Create a dictionary for this address
        row_dict = {'Address': address}
        
        # Add each record as Date_1, Action_1, Units_1, Price_1, Date_2, etc.
        for idx, (_, record) in enumerate(group.iterrows(), start=1):
            row_dict[f'Date_{idx}'] = record['Date']
            row_dict[f'Action_{idx}'] = record['Action']
            row_dict[f'Units_{idx}'] = record['Units']
            row_dict[f'Price_{idx}'] = record['Price']
        
        result_data.append(row_dict)
    
    # Create the result dataframe
    result_df = pd.DataFrame(result_data)
    
    # Organize columns in order: Address, Date_1, Action_1, Units_1, Price_1, Date_2, ...
    address_col = ['Address']
    other_cols = [col for col in result_df.columns if col != 'Address']
    
    # Sort the columns to get proper order
    sorted_cols = []
    for i in range(1, max_records + 1):
        if f'Date_{i}' in other_cols:
            sorted_cols.extend([f'Date_{i}', f'Action_{i}', f'Units_{i}', f'Price_{i}'])
    
    final_cols = address_col + sorted_cols
    result_df = result_df[final_cols]
    
    print(f"\nReorganized data shape: {result_df.shape}")
    print(f"Number of unique addresses: {len(result_df)}")
    
    # Save to Excel
    print(f"\nSaving to '{output_file}'...")
    result_df.to_excel(output_file, index=False, sheet_name='Reorganized')
    
    print("\n✅ Done! File saved successfully.")
    print(f"\nPreview of first 3 rows:")
    print(result_df.head(3))
    
    return result_df


if __name__ == "__main__":
    # File paths
    input_file = 'Conversion-Phase-2.xlsx'
    output_file = 'Conversion_Phase_2_Reorganized.xlsx'
    
    # Run the reorganization
    result = reorganize_data(input_file, output_file, sheet_name='Sorted')
    
    print("\n" + "="*70)
    print("SUMMARY:")
    print("="*70)
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print(f"Total addresses processed: {len(result)}")
    print(f"Total columns in output: {len(result.columns)}")