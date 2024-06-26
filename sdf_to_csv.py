import argparse
from rdkit import Chem
from rdkit.Chem import Descriptors
import pandas as pd
import gzip
import sys

def sdf_to_csv(sdf_file, csv_file):
    """
    Convert an SDF or gzipped SDF file to a CSV file, extracting the compound ID, Docking Score, SMILES code,
    and adding an index starting from 1.
    """
    # Use the docking score property name directly without brackets
    docking_score_property = "r_i_docking_score"

    if sdf_file.endswith('.gz'):
        # For gzipped files, open with gzip in binary mode and use ForwardSDMolSupplier
        with gzip.open(sdf_file, 'rb') as f:
            mol_supplier = Chem.ForwardSDMolSupplier(f)
            data = process_molecules(mol_supplier, docking_score_property)
    else:
        # For regular SDF files, use SDMolSupplier directly on the file path
        mol_supplier = Chem.SDMolSupplier(sdf_file)
        data = process_molecules(mol_supplier, docking_score_property)

    # Convert the list to a DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)

def process_molecules(mol_supplier, docking_score_property):
    """
    Process molecules from the supplier to extract Compound ID, Docking Score, SMILES code, and Index.
    """
    data = []
    index = 1  # Start index from 1
    for mol in mol_supplier:
        if mol is not None:
            compound_id = mol.GetProp('_Name')
            docking_score = mol.GetProp(docking_score_property) if mol.HasProp(docking_score_property) else "N/A"
            smiles_code = Chem.MolToSmiles(mol)  # Generate SMILES code
            molecular_weight = Descriptors.MolWt(mol)
            data.append({
                "Pose_num": index,
                "Compound_ID": compound_id,
                "Docking_Score": docking_score,
                "SMILES": smiles_code,
                "Mol_Weight": molecular_weight
            })
            index += 1  # Increment index for each molecule
    return data

def main():
    parser = argparse.ArgumentParser(description='Convert SDF or gzipped SDF to CSV, extracting Compound ID, Docking Score, SMILES code, and Index',
                                     usage='python %(prog)s input_file.sdf(.gz) output_file.csv')
    parser.add_argument('sdf_file', type=str, help='Input SDF or gzipped SDF file path')
    parser.add_argument('csv_file', type=str, help='Output CSV file path')
    args = parser.parse_args()

    try:
        sdf_to_csv(args.sdf_file, args.csv_file)
        print(f"CSV file generated: {args.csv_file}")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Ensure the input file exists and has the correct format.")
        sys.exit(1)

if __name__ == '__main__':
    main()
