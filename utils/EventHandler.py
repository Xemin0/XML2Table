import tkinter as tk
import numpy as np
from tkinter import simpledialog, messagebox

from .xml_processing.xml_parser import names_and_values


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
        self.renderTable2()

    def renderTable(self):
        """
        Subroutine for v01
        render the Table based on self.names and self.table as an upper-triangular one
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

    def renderTable2(self):
        """
        Subroutine for v02
        - Showing the full table instead of just the upper part above the main diagonal
        - The values will also get colors based on their relative difference
        - Symmetric Entries are now dynamically synced
        """
        if 1 == len(self.names):
            tk.Label(master = self.frame4table, text = self.names[0], foreground = 'purple').grid(row = 0, column = 1) # top row
            tk.Label(master = self.frame4table, text = self.names[0], foreground = 'purple').grid(row = 1, column = 0) # Leftmost column

            self.entries = []
            entry = tk.Entry(master = self.frame4table, width = 5)
            entry.grid(row = 1, column = 1)
            entry.insert(0, self.table[0,0])
            # set the initial color ???
            #color = self.compute_color(self.table[0,0], )
            self.entries.append([entry, None])


        else:
            #N = len(self.names)
            # Create and place the Label widgets for the names
            for i, name in enumerate(self.names):
                tk.Label(master = self.frame4table, text = name, foreground = 'purple').grid(row = 0, column = i+1) # top row
                tk.Label(master = self.frame4table, text = name, foreground = 'purple').grid(row = i+1, column = 0) # Leftmost column

            # Create and place the Entry widgets for the matrix values (contact energies)
            self.entries = []  # clear the old widgets

            self.min_val = self.table.min()
            self.max_val = self.table.max()

            # Diagonal Entries
            self.diag_entries = []
            for i in range(len(self.names)):
                row_entries = []
                for j in range(len(self.names)):
                    if i <= j: # Only show the upper triangular part
                        if i == j:
                            ###
                            ### Need Review for optimization
                            ###
                            entry = tk.Entry(master = self.frame4table, width = 5)
                            entry.grid(row = i+1, column = j+1)
                            entry.insert(0, self.table[i,j])    # show current value

                            # apply an initial color for values positive                                     
                            #if self.table[i,j] > 0: # Excluding non-positive values
                            color = self.compute_color(self.table[i,j], self.min_val, self.max_val)
                            entry.configure(bg = color)
                            # if the color range of the bg is light, need to set the text color to black
                            entry.configure(foreground = "black")

                            self.diag_entries.append(entry) # Store the created entry for event function binding

                            # bind entry with event function that dynamically change its bg color based on its value
                            #### Pass i as a default argument to the lambda
                            self.diag_entries[i].bind('<KeyRelease>', lambda event, idx = i: self.change_color(self.diag_entries[idx], (idx,idx)))

                            row_entries.append([entry, None])
                        else: # i < j then create synchronized entries
                            twin_entries = self.synced_entries(master = self.frame4table,
                                                              compute_color_func = self.compute_color,
                                                              table = self.table, # numpy object passed by reference
                                                              indices = (i, j),
                                                              width = 5)

                            # visually place the entries accordingly
                            twin_entries.entry1.grid(row = i+1, column = j+1)
                            twin_entries.entry2.grid(row = j+1, column = i+1)
                            # Set values according to the matrix
                            twin_entries.entry1.insert(0, self.table[i,j])
                            twin_entries.entry2.insert(0, self.table[i,j])
                            # apply an initial color for values positive
                            #if self.table[i,j] > 0: # whether excluding non-positive values
                            color = self.compute_color(self.table[i,j], self.min_val, self.max_val)
                            twin_entries.entry1.configure(bg = color)
                            twin_entries.entry2.configure(bg = color)

                            # if the color range of the bg is light, need to set the text color to black
                            twin_entries.entry1.configure(foreground = "black")
                            twin_entries.entry2.configure(foreground = "black")

                            row_entries.append([twin_entries.entry1, twin_entries.entry2])

                            ## Bind Color Changing Event function to the synced entries
                            #self.entries[i][j-i][0].bind('<KeyRelease>', lambda event, indices = (i, j): self.change_color(self.entries[i][j-i][0], indices))
                            #self.entries[i][j-i][1].bind('<KeyRelease>', lambda event, indices = (j, i): self.change_color(self.entries[i][j-i][1], indices))

                self.entries.append(row_entries)


            for i in range(len(self.names)):
                for j in range(len(self.names)):
                    if i < j:
                        ## Bind Color Changing Event function to the synced entries
                        self.entries[i][j-i][0].bind('<KeyRelease>', lambda event, idi = i, idj = j: self.change_color(self.entries[idi][idj - idi][0], (idi, idj)))
                        self.entries[i][j-i][1].bind('<KeyRelease>', lambda event, idi = i, idj = j: self.change_color(self.entries[idi][idj - idi][1], (idi, idj))) # Still pass in (i, j) for simple downstream value-syncing operation



    def compute_color(self, value, min_val, max_val):
        """
        Subroutine
        compute the color based on the value's relative position between min and max
        """

        # max_val != min_val
        if min_val == max_val:
            ratio = 0
        else:
            ratio = (value - min_val) / (max_val - min_val)
        red = int(255 * ratio)
        green = int(255 * (1 - ratio))
        blue = 180
        return f'#{red:02x}{green:02x}{blue:02x}'

    def change_color(self, src, indices):
        """
        Event Function to change the color of entries based on their relative position between min and max in the matrix
            - Update Entry Value
            - Update min_max Record
            - Change Entry Pair Colors
            - ** Update the color for the whole table
        """
        value = float(src.get())
        # update the min_max record
        #if value < self.min_val:
        #    self.min_val = value
        #if value > self.max_val:
        #    self.max_val = value
        # update the table 
        i, j = indices
        #print(" i = ", i)
        #print(" j = ", j)
        self.table[i, j] = self.table[j, i] = value
        self.min_val, self.max_val = self.table.min(), self.table.max()

        # Syncing Values
        ##
        ## ** A better way would be passing the synced_entries object in, instead of passing in them as a list
        if i != j: # Then i < j is assumed
            entry1 = self.entries[i][j-i][0]
            entry2 = self.entries[i][j-i][1]
            if src == entry1:
                entry2.delete(0, tk.END)
                entry2.insert(0, value)
            else:
                entry1.delete(0, tk.END)
                entry1.insert(0, value)

        # Compute the color
        #color = self.compute_color(value, self.min_val, self.max_val)
        #src.configure(bg = color)
        #print("updated_table = \n", self.table)
        # Color the whole table
        self.color_whole_table()


    def color_whole_table(self):
        """
        Subroutine
        Color the whole table of entries based on current matrix values
        """
        N = len(self.names)
        #self.min_val, self.max_val = self.table.min(), self.table.max()
        for i in range(N):
            for j in range(N):
                if i <= j:
                    color = self.compute_color(self.table[i,j], self.min_val, self.max_val)
                    entry1, entry2 = self.entries[i][j-i]
                    # Set the color for both entries
                    entry1.configure(bg = color)
                    if entry2 is not None:
                        entry2.configure(bg = color)


    def updateMatrix(self):
        """
        Subroutine
        Update the stored matrix values based on edited Entry fields
        """
        for i in range(len(self.names)):
            for j in range(len(self.names)):
                if i <= j: # Only use the upper triangular part
                    value = self.entries[i][j - i][0].get()
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
                    self.renderTable2()
                    break




    def clearTable(self):
        """
        Clear the table Contents
        """
        for widget in self.frame4table.winfo_children():
            widget.destroy()
        self.names = []
        self.table = None

    def clearFrame(self, frame):
        """
        Clear the frame for re-rendering
        """
        for widget in frame.winfo_children():
            widget.destroy()



    class synced_entries:
        """
        Create Two Synced Entries that Share the Same Entry Value and the Same BG Color
        *** Consider inherit from tk.Entry ***
        """
        def __init__(self, master, compute_color_func, table, indices, width = 5):
            self.entry1 = tk.Entry(master = master, width = width)
            self.entry2 = tk.Entry(master = master, width = width)

            self.compute_color = compute_color_func
            # Original matrix
            self.table = table
            self.min_val, self.max_val = self.table.min(), self.table.max()
            # entry position inside the matrix
            self.i, self.j = indices

            # Bind them with sync method
            #self.entry1.bind('<KeyRelease>', lambda event: self.sync(self.entry1))
            #self.entry2.bind('<KeyRelease>', lambda event: self.sync(self.entry2))

        def sync(self, src):
            """Event Function to sync the entries based on the source entry """
            value = float(src.get())
            # update the min_max record
            #if value < self.min_val:
            #    self.min_val = value
            #if value > self.max_val:
            #    self.max_val = value
            # update the table entry pair
            #self.table[self.i, self.j] = self.table[self.j, self.i] = value
            #self.min_val, self.max_val = self.table.min(), self.table.max()


            #### The coloring part will be handled as an extra event function in the outter class
            ####
            #color = self.compute_color(value, self.min_val, self.max_val)
            # Change current entry's color
            #src.configure(bg = color)

            if src == self.entry1:
                self.entry2.delete(0, tk.END)
                self.entry2.insert(0, value)
                # change the twin entry's color
                #self.entry2.configure(bg = color)
            else:
                self.entry1.delete(0, tk.END)
                self.entry1.insert(0, value)
                # change th twin entry's color
                #self.entry1.configure(bg = color)
