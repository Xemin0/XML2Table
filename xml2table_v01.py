"""
Front-end GUI for the python app XML2Table
to facilitate the Contact Energy Plugin settings in XML generated in CompuCell3D

Visual Compenents and their usages (Left to Right)
    - Text Field for XML(Contact Energy Plugin):
        - XML section copy-pasted from CC3D.twedit to be converted to table
          or
        - XML section generated based on the adjusted table
    - Four Buttons:
        - Convert XML to Table
        - Generate XML from Table
        - Add a New Cell
        - Clear the Table
    - Table Field:
"""
import tkinter as tk
from EventHandler import EventHandler

"""
# Base window
"""

window = tk.Tk()
window.title("Simple XML2Table Editor")

# Set minimal Size to ensure the texts in the buttons will be shown properly
window.rowconfigure(0, minsize = 200, weight = 1)
window.columnconfigure(0, minsize = 100, weight = 1)
window.columnconfigure(1, minsize = 150, weight = 1)
window.columnconfigure(2, minsize = 100, weight = 1)

# ====================================== #



"""
# Create Frames for each region and attach them to the main window horizontally
# with default sizes
"""

frame_txtField = tk.Frame(master = window, width = 60, height = 200)

frame_buttons = tk.Frame(master = window, relief = tk.RAISED, bd = 2, width = 20, height = 200)

frame_table = tk.Frame(master = window, width = 100, height = 200)

# ====================================== #


"""
# Arrange the Fields/Widgets accordingly inside the main window
"""
#frame_txtField.pack(fill = tk.BOTH, side = tk.LEFT, expand = True)
#frame_buttons.pack(fill = tk.Y, side = tk.LEFT, expand = True)
#frame_table.pack(fill = tk.BOTH, side = tk.LEFT, expand = True)

frame_txtField.grid(row = 0, column = 0, sticky = 'nsew')
frame_buttons.grid(row = 0, column = 1, sticky = 'ns')
frame_table.grid(row = 0, column = 2, sticky = 'nsew')

# ====================================== #



"""
# Text Field for XML
"""

text_box = tk.Text(master = frame_txtField) # height = 10, width = 20)

# Place text field inside the frame
text_box.pack(fill = tk.BOTH, expand = True)

# ====================================== #
"""
# Event Handler Class Object
"""
e_handler = EventHandler(text_box, frame_table)

# ====================================== #




"""
# Buttons
    - convert to table
    - convert to XML
    - add new cell
    - clear table

# Event Handlers for each Button
"""


btn_xml2table = tk.Button(master = frame_buttons, text = 'Convert to Table', command = e_handler.toTable)
btn_table2xml = tk.Button(master = frame_buttons, text = 'Convert to XML', command = e_handler.toXML)
btn_newCell = tk.Button(master = frame_buttons, text = 'Add New Cell', command = e_handler.newCell)
btn_clear = tk.Button(master = frame_buttons, text = 'Clear Table', command = e_handler.clearTable)

# Place the three buttons inside the frame
#btn_xml2table.pack(fill = tk.Y, padx = 5)
#btn_table2xml.pack(fill = tk.Y, padx = 5)
#btn_newCell.pack(fill = tk.Y, padx = 5)

# Sticky = 'ew' to guarantee the buttons are all of the same width
btn_xml2table.grid(row = 0, column = 0, sticky = 'ew', padx = 5, pady = 5)
btn_table2xml.grid(row = 1, column = 0, sticky = 'ew', padx = 5, pady = 5)
btn_newCell.grid(row = 2, column = 0, sticky = 'ew', padx = 5, pady = 5)
btn_clear.grid(row = 3, column = 0, sticky = 'ew', padx = 5, pady = 5)


# ====================================== #

"""
# Table Field

** This part is not initialized by default, but will be updated once a related button event occurs
"""


window.mainloop()
