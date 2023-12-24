"""
(PyQt)Front-end GUI for the python app XML2Table
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
    - Color Bar Field:
    - Table Field:
"""
import sys
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTextEdit

if __name__ == "__main__":
    # running as a script
    from utils.EventHandler import EventHandler
    from visual_components.ColorBar import ColorBar
else:
    from .utils.EventHandler import EventHandler
    from .visual_components.ColorBar import ColorBar


def main():
    """
    # Base window
    """
    app = QApplication(sys.argv)
    mainWindow = XML2Table()
    mainWindow.show()
    sys.exit(app.exec_())


class XML2Table(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple XML2Table Editor")
        self.setMinimumSize(400, 320) # Set a minimum size for the window

        # ====================================== #
        # Main widget and a horizonatl layout for the major components
        self.mainWidget = QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.mainLayout = QHBoxLayout(self.mainWidget)

        # ====================================== #
        # Text Field for XML
        self.text_box = QTextEdit()
        self.mainLayout.addWidget(self.text_box)

        # ====================================== #
        """
        # Buttons
            - convert to table
            - convert to XML
            - add new cell
            - clear table

        # Event Handlers for each Button
        """
        self.frame_buttons = QWidget()
        self.buttonsLayout = QVBoxLayout(self.frame_buttons)
        self.mainLayout.addWidget(self.frame_buttons)

        self.buttonsLayout.setSpacing(15) # The space between the buttons
        self.buttonsLayout.setContentsMargins(5, 5, 5, 5) # left, top, right, bottom
        # ====================================== #
        # Create EventHandler Instance
        self.tableLayout = QVBoxLayout()
        self.e_handler = EventHandler(self.text_box, self.tableLayout)

        # ====================================== #
        # Define buttons and add to layout
        self.btn_xml2table = QPushButton('Convert to Table', self)
        self.btn_xml2table.clicked.connect(self.e_handler.toTable)
        self.buttonsLayout.addWidget(self.btn_xml2table)

        self.btn_table2xml = QPushButton('Convert to XML', self)
        self.btn_table2xml.clicked.connect(self.e_handler.toXML)
        self.buttonsLayout.addWidget(self.btn_table2xml)

        self.btn_newCell = QPushButton('Add New Cell', self)
        self.btn_newCell.clicked.connect(self.e_handler.newCell)
        self.buttonsLayout.addWidget(self.btn_newCell)

        self.btn_clear = QPushButton('Clear Table', self)
        self.btn_clear.clicked.connect(self.e_handler.clearTable)
        self.buttonsLayout.addWidget(self.btn_clear)

        # Add a Space at the bottom to push the buttons up (top-aligned)
        btn_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding) # W, H, 
        self.buttonsLayout.addItem(btn_spacer)

        # ====================================== #
        # Color Bar
        self.color_bar = ColorBar(parent = self, compute_color_func = self.e_handler.compute_color, W = 25, H = 200)
        self.mainLayout.addWidget(self.color_bar)


        # ====================================== #
        # Table Field 
        # (Not initialized by default until the corresponding button is clicked)
        self.mainLayout.addLayout(self.tableLayout)


if __name__ == "__main__":
    main()
