# generates a .txt file with each compoundID/name (1 per line)
# maintains original order/rank
# this is used during enrichment analysis (with Peter Ung's code)

from rdkit import Chem
import argparse
import gzip
import os

def get_compound_names(input, output):
    compound_names = []
    
    if input.endswith('.gz'):
        with gzip.open(input, 'rb') as f:
            suppl = Chem.ForwardSDMolSupplier(f)
            for mol in suppl:
                if mol is not None:
                    name = mol.GetProp('_Name')
                    compound_names.append(name)
    else:
        with open(input, 'rb') as f:
            suppl = Chem.ForwardSDMolSupplier(f)
            for mol in suppl:
                if mol is not None:
                    name = mol.GetProp('_Name')
                    compound_names.append(name)

    with open(output, 'w') as file:
        for name in compound_names:
            file.write(str(name) + '\n')

def main():
    parser = argparse.ArgumentParser(description = 'Convert sdf to txt file with list of ranked compound names')
    parser.add_argument('input', type=str, help = 'Input sdf file')
    
    args=parser.parse_args()

    # making the output file the same filename but with .txt instead
    base_name = os.path.splitext(args.input)[0]
    # in the case of .sdf.gz:
    if base_name.endswith('.sdf'):
        base_name = os.path.splitext(base_name)[0]

    output = base_name + '.txt'

    try:
        get_compound_names(args.input, output)
        print(f"TXT file generated: {output}")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Ensure the input file exists and has the correct format.")
        sys.exit(1)
    
if __name__ == "__main__":
    main()

