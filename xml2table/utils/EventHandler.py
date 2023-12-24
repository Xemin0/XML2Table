import numpy as np
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QInputDialog
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QColorDialog
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt

from .xml_processing.xml_parser import names_and_values


"""
    Buttons for the Button-Frame
    Event Handlers for each Button
"""

class EventHandler:
    def __init__(self, text_box, frame4table, *args):
        self.text_field = text_box    # QTextEdit to extract the raw XML from
        self.frame4table = frame4table # The Layout to render the editable table 

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
        self.rawXML = self.text_field.toPlainText()
        if self.rawXML:
            self.names, self.table = names_and_values(self.rawXML)
            # Create the table and render it inside the corresponding frame
            self.renderTable2()


    def adjustTableSize(self):
        '''
        Set the size for each table cell
        Then set the minimum size of the resulting table
        '''
        cellW = 50
        cellH = 30

        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHeight(i, cellH)
        for j in range(self.tableWidget.columnCount()):
            self.tableWidget.setColumnWidth(j, cellW)

        totalW = self.tableWidget.columnCount() * cellW
        totalH = self.tableWidget.rowCount() * cellH

        self.tableWidget.setMinimumSize(totalW, totalH)

    def renderTable2(self):
        """
        Subroutine for v02
        - Showing the full table instead of just the upper part above the main diagonal
        - The values will also get colors based on their relative difference
        - Symmetric Entries are now dynamically synced
        """
        # Font
        font = QFont()
        font.setPointSize(15)
        # Initialize the table with labels
        self.tableWidget = QTableWidget(len(self.names), len(self.names))

        self.tableWidget.setHorizontalHeaderLabels(self.names)
        self.tableWidget.horizontalHeader().setFont(font)

        self.tableWidget.setVerticalHeaderLabels(self.names)
        self.tableWidget.verticalHeader().setFont(font)

        if self.table is None:
            self.min_val, self.max_val = 0, 0
        else:
            self.min_val, self.max_val = self.table.min(), self.table.max()

        # Populate the table
        for i in range(len(self.names)):
            for j in range(len(self.names)):
                item = QTableWidgetItem(str(self.table[i,j]))
                self.tableWidget.setItem(i, j , item)
                # Set initial color
                color = self.compute_color(self.table[i, j], self.min_val, self.max_val)
                item.setBackground(QColor(color))

                #self.tableWidget.item(i, j).setData(Qt.UserRole, (i, j)) # Keep a record of the indices for current item

        # Connect cell editing signal to color change and synchronization functions
        self.tableWidget.cellChanged.connect(self.onCellChanged)

        # Adjust the size of table cells
        self.adjustTableSize()
        # clear the frame4table sublayout if it already has widgets
        self.clearLayout(self.frame4table)
        self.frame4table.addWidget(self.tableWidget) # Add table to the sublayout

    def onCellChanged(self, row, column):
        # Get the new value from the edited cell 
        #### Use a QMessageBox to handle the exception
        try:
            text = self.tableWidget.item(row, column).text()
            new_val = float(text)

            print('The update matrix is:\n', self.table)

            # 1. Update the symmetric cell
            self.tableWidget.blockSignals(True)
            symmetric_item = self.tableWidget.item(column, row)
            if symmetric_item:
                symmetric_item.setText(str(new_val))
            self.tableWidget.blockSignals(False)

            # 2. Update the data matrix
            self.table[row, column] = new_val
            self.table[column, row] = new_val

            # 3. Recalculate and apply colors
            self.recolorTable()
        except ValueError:
            print(f"Invalid value at row {row + 1}, column {column + 1}: {text}")



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

    def recolorTable(self):
        """
        Event Function to change the color of entries based on their relative position between min and max in the matrix
            - Update Entry Value
            - Update min_max Record
            - Change Entry Pair Colors
            - ** Update the color for the whole table
        """
        self.min_val, self.max_val = self.table.min(), self.table.max()
        for i in range(len(self.names)):
            for j in range(len(self.names)):
                item = self.tableWidget.item(i, j)
                if item:
                    color = self.compute_color(self.table[i, j], self.min_val, self.max_val)
                    item.setBackground(QColor(color))

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

#===================================================# 

    def toXML(self):
        """
        Convert the edited n-by-n table to XML

        *** Simply just replace the variable strings
        """
        if self.table is None:
            QMessageBox.warning(None, "Error", "Copy paste here the XML content first!")
            return

        # Initialize the output text
        self.rawXML = ''
        for i, name1 in enumerate(self.names):
            for j, name2 in enumerate(self.names):
                if i <= j: # Upper Triangular part
                    self.rawXML += self.xml_format[0] + name1 + self.xml_format[1] + name2 + self.xml_format[2] + str(self.table[i,j]) + self.xml_format[3] + '\n'
            self.rawXML += '\n'

        # Clear the text edit first and render the new XML
        self.text_field.clear()
        self.text_field.setPlainText(self.rawXML)


#===================================================# 

    def newCell(self):
        """
        Add a new cell type to the table
            1. pop up a new window with Entry field waiting for usr input ** To be replaced by a better logic **
            2.1. if the table is empty, build the table with new columns and rows (and the corresponding XML strings will be constructed from harded coded presets, instead of modifying from existing texts)
            2.2 if the table is not empty, add new a new column

        An extra row and an extra column will be added in the table with the new cell type    """
        while True:
            # Show input dialog to get user input
            user_input, ok = QInputDialog.getText(None, "Cell Name", "Enter the Name of the New Cell Type")
            if ok and user_input:
                if user_input in self.names:
###
                    QMessageBox.warning(None, "Warning", "The Cell Name Already Exists, Please Enter a New One.")
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


#===================================================# 


    def clearLayout(self, layout):
        """
        Clear all widgets from a layout
        """
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def clearTable(self):
        """
        Clear the table Contents
        """
        '''
        if self.tableWidget is not None:
            self.frame4table.removeWidget(self.tableWidget)
            self.tableWidget.deleteLater()
            self.tableWidget = None
        '''
        self.clearLayout(self.frame4table)
        self.names = []
        self.table = None


#===================================================# 
