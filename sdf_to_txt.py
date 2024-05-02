#!/usr/bin/env python
# coding: utf-8

# In[1]:


from rdkit import Chem
import argparse


# In[ ]:


def get_compound_names(input, output):
    suppl = Chem.SDMolSupplier(input)
    compound_names = []
    for mol in suppl:
        if mol is not None:
            name = mol.GetProp('_Name')
            compound_names.append(name)
    with open(output, 'w') as file:
        for name in compound_names:
            file.write(str(name) + '\n')


# In[ ]:


def main():
    parser = argparse.ArgumentParser(description = 'Convert sdf to txt file with list of ranked compound names')
    parser.add_argument('input', type=str, help = 'Input sdf file')
    parser.add_argument('output', type=str, help = 'Output txt file')
    
    args=parser.parse_args()
    
    get_compound_names(args.input, args.output)
    
if __name__ == "__main__":
    main()

