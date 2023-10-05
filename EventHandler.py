import tkinter as tk
import numpy as np
from xml_processing.xml_parser import names_and_values
from tkinter import simpledialog, messagebox


"""
    Buttons for the Button-Frame
    Event Handlers for each Button
"""

class EventHandler:
    def __init__(self, text_field, frame4table, *args):
        self.text_field = text_field    # Text Field to extract the raw XML from
        self.frame4table = frame4table  # The frame to render the editable table
        self.entries = []               # references to Entry widgets created


        self.rawXML = None          # Raw XML string extracted
        self.xml_format = ['''<Energy Type1="''',
                          '''" Type2="''',
                          '''">''',
                          '''</Energy>''']      # Parsed single-line const string to set contact energies between any two cells.
                                    # Could be Hard-Coded
        ##
        ## !! Does not support setting IDs for energies if hard-coded!! 
        ## 

        self.names = []           # List of cell names parsed from XML
        self.table = None           # An upper triangular or symmetric (numpy) matrix to represent the contact energies between every two of the cells.


    def toTable(self):
        """
        Convert the XML in the text field into a n-by-n (upper-triangular) table:
            1. Retrieve the XML in the text field
            2. Parse XML to check the number of unique cell types, while saving the constant/variable strings for later reconstruction of the XML based on the edited table  *** To be replaced by standard parsing methods ***
                2.1. Constant Strings (base XML format) *** To be replace by standard methods to transfer these values across this widget ***
                2.2. Variables
                    2.2.1 Cell Types
                    2.2.2 Energy Values
            3. create a n-by-n table with cell types as the first column and the first row, for n unique cell types in the XML

        *** Table is currently implemented as grids of Labels and Entrys ***
        """
        # Get the Raw XML from the text box
        self.rawXML = self.text_field.get("1.0", tk.END) # Line number starts at 1
                                                         # Char count starts at 0
        self.names, self.table = names_and_values(self.rawXML)
        # Create the table and render it inside the corresponding frame
        self.renderTable()

    def renderTable(self):
        """
        Subroutine
        render the Table based on self.names and self.table
        """
        # primarily using the .grid method

        if 1 == len(self.names):
            tk.Label(master = self.frame4table, text = self.names[0], foreground = 'purple').grid(row = 0, column = 1) # top row
            tk.Label(master = self.frame4table, text = self.names[0], foreground = 'purple').grid(row = 1, column = 0) # Leftmost column

            self.entries = []
            entry = tk.Entry(master = self.frame4table, width = 5)
            entry.grid(row = 1, column = 1)
            entry.insert(0, self.table[0,0])
            self.entries.append([entry])

        else:
            # Create and place the Label widgets for the names
            for i, name in enumerate(self.names):
                tk.Label(master = self.frame4table, text = name, foreground = 'purple').grid(row = 0, column = i+1) # top row
                tk.Label(master = self.frame4table, text = name, foreground = 'purple').grid(row = i+1, column = 0) # Leftmost column

            # Create and place the Entry widgets for the matrix values (contact energies)
            self.entries = []  # clear the old widgets
            for i in range(len(self.names)):
                row_entries = []
                for j in range(len(self.names)):
                    if i <= j: # Only show the upper triangular part
                        entry = tk.Entry(master = self.frame4table, width = 5)
                        entry.grid(row = i+1, column = j+1) # location inside the frame
                        entry.insert(0, self.table[i,j])    # show current value
                        row_entries.append(entry)
                self.entries.append(row_entries)



    def updateMatrix(self):
        """
        Subroutine
        Update the stored matrix values based on edited Entry fields
        """
        for i in range(len(self.names)):
            for j in range(len(self.names)):
                if i <= j: # Only use the upper triangular part
                    value = self.entries[i][j - i].get()
                    try:
                        self.table[i,j] = self.table[j,i] = float(value)
                    except ValueError:
                        print(f"Invalid value at rwo {i + 1}, column {j+1}: {value}")

        print('The update matrix is:\n', self.table)

    def toXML(self):
        """
        Convert the edited n-by-n table to XML

        *** Simply just replace the variable strings
        """
        if self.table is None:
            raise Exception("Copy paste here the XML content first!")
        else:
            # Update the stored matrix based on values in each Entry field
            self.updateMatrix()
            # Initialize the output text
            self.rawXML = ''
            for i, name1 in enumerate(self.names):
                for j, name2 in enumerate(self.names):
                    if i <= j: # Upper Triangular part
                        self.rawXML += self.xml_format[0] + name1 + self.xml_format[1] + name2 + self.xml_format[2] + str(self.table[i,j]) + self.xml_format[3] + '\n'
                self.rawXML += '\n'

            # Render it inside the text field
            # Clear the text field first
            self.text_field.delete("1.0", tk.END) # Line number starts at 1, character count starts at 0
            self.text_field.insert("1.0", self.rawXML)



    def newCell(self):
        """
        Add a new cell type to the table
            1. pop up a new window with Entry field waiting for usr input ** To be replaced by a better logic **
            2.1. if the table is empty, build the table with new columns and rows (and the corresponding XML strings will be constructed from harded coded presets, instead of modifying from existing texts)
            2.2 if the table is not empty, add new a new column

        An extra row and an extra column will be added in the table with the new cell type    """
        while True:
            user_input = simpledialog.askstring("Cell Name", "Enter the Name of the New Cell Type")
            if user_input:
                if user_input in self.names:
                    messagebox.showwarning("Warning", "The Cell Name Already Exists, Please Enter a New One.")
                else:
                    # Append it to the list of cell types
                    self.names.append(user_input)
                    # Expand the matrix with an extra row and column
                    N = len(self.names)
                    if self.table is not None:
                        mat = np.zeros((N, N), dtype = float)
                        mat[:-1, :-1] = self.table
                        self.table = mat
                    else:
                        self.table = np.zeros((1,1), dtype = float)
                    # Render the matrix into table 
                    self.renderTable()
                    break




    def clearTable(self):
        """
        Clear the table Contents
        """
        for widget in self.frame4table.winfo_children():
            widget.destroy()
        self.names = []
        self.table = None

