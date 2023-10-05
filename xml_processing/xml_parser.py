"""
Utilities to Parse XML


For further improvements all methods should use Regular Expressions
or designated XML parsing methods in python
"""
import numpy as np
import re


"""
Example XML format for contact energy:

<Plugin Name="Contact">
  <!-- Specification of adhesion energies -->
  <Energy Type1="Medium" Type2="Medium">10.0</Energy>

  <NeighborOrder>4</NeighborOrder>
</Plugin>


Intended Approach: using .split method to get
    - the cell names for each type ("Type1" and "Type2") marked by quotation mark "
    - the contact energy marked by >
    - the const strings

Or use Regular Expression re Module
"""

def getNames(xml):
    """
    Parse XML and return a list of unique Cell Names
    """
    names = []
    # for each line
    for line in xml.split('\n'):
       str_list = line.split('"')
       names += [str_list[1]] + [str_list[3]]
    return set(names)

def names_and_values(xml):
    """
    Extract unique cell names and energies between every two of them
    Input:
        - XML: the raw XML texts
    Output:
        - unique_names: unique cell names
        - mat: a symmetric adjacent matrix for corresponding contact energies between every two cell types
    """
    edges = [] # Store (value, celltype1, celltype 2) as edges 

    # for each line
    #i = 0
    for line in xml.split('\n'):
        #print('at line-', i)
        # Only process the lines that start with <Energy
        # using regular expression module
        match = re.search(r'<\s*(\w+)', line) # Checking the first captured group after each '<'
        #i += 1
        if (match is not None) and (match.group(1) == 'Energy'):
            #str_list = line.split('"')

            """
            # Number between the first > < pair
            # integer or decimals or decimals without leading digits
            """
            #value = float(str_list[-1].split('>')[1].split('<')[0] # or using re module
            value = re.search(r'>\s*(\d*(\.\d+)?)\s*<', line).group(1)
            """
            # Matches names inside either pairing single- or double-quotation marks after the = sign
            # names support all characters other than quotation marks
            # ignoring all spaces after and before quotation marks
            """
            names = re.findall(r'''=\s*([\"'])\s*([^"\']+)\s*\1''', line)
            #name1 = str_list[1]
            #name2 = str_list[3]
            name1 = (names[0])[1]
            name2 = (names[1])[1]

            edges.append([value, name1, name2])

    unique_names = list(set(t[1] for t in edges) | set(t[2] for t in edges))
    # Re-arrange to make 'Medium' the default type to be the first, if included
    if 'Medium' in unique_names:
        unique_names.remove('Medium')
        unique_names.insert(0, 'Medium')

    N = len(unique_names) # number of unique cell types

    # construct the adjacent matrix and fill in the values
    ## It is a symmetric matrix, and we will only use the upper-triangular part
    mat = np.zeros((N, N), dtype = float)
    # Try to Fill in the Values
    for t in edges:
        try:
            i = unique_names.index(t[1]) # Corresponding contact energies / indices in the matrix
            j = unique_names.index(t[2])
        except ValueError:
            print(f"Either '{t[1]}' or '{t[2]}'  is not in the unique_names !!")
        mat[i,j] = mat[j,i] = t[0]

    return unique_names, mat
