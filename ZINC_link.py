# adds ZINC entry link as a column in spreadsheet generated with sdf_to_csv.py

import pandas as pd
import argparse

def add_zinc_links_in_place(csv_file):
    """
    Add ZINC entry links to the CSV file based on the Compound ID, modifying the file in place.

    Parameters:
    - csv_file: Path to the CSV file to be modified.
    """
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Define a function to create the ZINC link
    def create_zinc_link(compound_id):
        # Format the compound ID to fill in the trailing zeros
        formatted_id = f"ZINC{int(compound_id):012d}"
        return f"https://zinc.docking.org/substances/{formatted_id}/"

    # Apply the function to create a new column for ZINC links
    df['ZINC_Link'] = df['Compound_ID'].apply(create_zinc_link)

    # Save the updated DataFrame back to the same CSV file, overwriting it
    df.to_csv(csv_file, index=False)

def main():
    parser = argparse.ArgumentParser(description='Add ZINC entry links to a CSV file based on Compound IDs, modifying in place')
    parser.add_argument('csv_file', type=str, help='CSV file path to be modified in place')
    args = parser.parse_args()

    try:
        add_zinc_links_in_place(args.csv_file)
        print(f"CSV file modified in place: {args.csv_file}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
