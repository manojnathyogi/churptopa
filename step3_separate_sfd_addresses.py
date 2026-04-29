import pandas as pd
import numpy as np

def separate_sfd_addresses(input_file, output_sfd_file, output_non_sfd_file):
    """
    Separate addresses based on whether they have any SFD (Single Family Dwelling) actions.
    
    Parameters:
    -----------
    input_file : str
        Path to input Excel file (reorganized data)
    output_sfd_file : str
        Path to output Excel file for addresses WITH SFD actions
    output_non_sfd_file : str
        Path to output Excel file for addresses WITHOUT SFD actions
    """
    
    # Define the SFD actions to look for
    sfd_actions = [
        'SFD Claim of Elderly or Disabled Status',
        'SFD Letter to Landlord',
        'SFD Notice of Solicitation of Offer & Notice of Intent to Sell',
        'SFD Notice of Transfer',
        'SFD Offer of Sale w/ Contract',
        'SFD Offer of Sale w/o Contract',
        'SFD Right of First Refusal'
    ]
    
    print("="*70)
    print("SEPARATING ADDRESSES BASED ON SFD ACTIONS")
    print("="*70)
    
    print(f"\nLoading data from '{input_file}'...")
    df = pd.read_excel(input_file)
    
    print(f"Total addresses in file: {len(df)}")
    print(f"\nLooking for these SFD actions:")
    for i, action in enumerate(sfd_actions, 1):
        print(f"  {i}. {action}")
    
    # Get all Action columns
    action_columns = [col for col in df.columns if col.startswith('Action_')]
    print(f"\nTotal action columns to check: {len(action_columns)}")
    
    # Create a boolean mask for addresses with SFD actions
    has_sfd_action = []
    sfd_details = []
    
    for idx, row in df.iterrows():
        found_sfd = False
        sfd_actions_found = []
        
        # Check all action columns for this address
        for action_col in action_columns:
            action_value = row[action_col]
            
            # Check if this action is in our SFD list
            if pd.notna(action_value) and action_value in sfd_actions:
                found_sfd = True
                sfd_actions_found.append(action_value)
        
        has_sfd_action.append(found_sfd)
        sfd_details.append({
            'Address': row['Address'],
            'Has_SFD': found_sfd,
            'SFD_Actions_Found': list(set(sfd_actions_found))  # Remove duplicates
        })
    
    # Add the boolean column to dataframe
    df['Has_SFD_Action'] = has_sfd_action
    
    # Separate the dataframes
    df_sfd = df[df['Has_SFD_Action'] == True].copy()
    df_non_sfd = df[df['Has_SFD_Action'] == False].copy()
    
    # Remove the helper column before saving
    df_sfd = df_sfd.drop('Has_SFD_Action', axis=1)
    df_non_sfd = df_non_sfd.drop('Has_SFD_Action', axis=1)
    
    print("\n" + "="*70)
    print("RESULTS:")
    print("="*70)
    print(f"✅ Addresses WITH SFD actions: {len(df_sfd)}")
    print(f"❌ Addresses WITHOUT SFD actions: {len(df_non_sfd)}")
    print(f"📊 Total: {len(df_sfd) + len(df_non_sfd)}")
    
    # Save the separated files
    print(f"\n💾 Saving SFD addresses to '{output_sfd_file}'...")
    df_sfd.to_excel(output_sfd_file, index=False, sheet_name='SFD_Addresses')
    
    print(f"💾 Saving Non-SFD addresses to '{output_non_sfd_file}'...")
    df_non_sfd.to_excel(output_non_sfd_file, index=False, sheet_name='Non_SFD_Addresses')
    
    print("\n✅ Files saved successfully!")
    
    # Show some examples
    print("\n" + "="*70)
    print("EXAMPLES OF SFD ADDRESSES:")
    print("="*70)
    
    sfd_details_df = pd.DataFrame(sfd_details)
    sfd_examples = sfd_details_df[sfd_details_df['Has_SFD'] == True].head(5)
    
    for idx, example in sfd_examples.iterrows():
        print(f"\n📍 {example['Address']}")
        print(f"   SFD Actions: {', '.join(example['SFD_Actions_Found'])}")
    
    print("\n" + "="*70)
    print("EXAMPLES OF NON-SFD ADDRESSES:")
    print("="*70)
    
    non_sfd_examples = sfd_details_df[sfd_details_df['Has_SFD'] == False].head(5)
    
    for idx, example in non_sfd_examples.iterrows():
        print(f"\n📍 {example['Address']}")
        print(f"   No SFD actions found")
    
    # Show breakdown of SFD action types
    print("\n" + "="*70)
    print("SFD ACTION TYPE BREAKDOWN:")
    print("="*70)
    
    sfd_action_counts = {}
    for detail in sfd_details:
        if detail['Has_SFD']:
            for action in detail['SFD_Actions_Found']:
                sfd_action_counts[action] = sfd_action_counts.get(action, 0) + 1
    
    for action, count in sorted(sfd_action_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{action}: {count} addresses")
    
    return df_sfd, df_non_sfd


if __name__ == "__main__":
    # File paths
    input_file = 'Reorganized.xlsx'
    output_sfd_file = 'SFD_Addresses.xlsx'
    output_non_sfd_file = 'Non_SFD_Addresses.xlsx'
    
    # Run the separation
    df_sfd, df_non_sfd = separate_sfd_addresses(input_file, output_sfd_file, output_non_sfd_file)
    
    print("\n" + "="*70)
    print("✨ PROCESS COMPLETE!")
    print("="*70)