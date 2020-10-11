
merge_operations = {
    'atop': (True, False),
    'average': (True, False),
    'color-burn': (True, False),
    'color-dodge': (True, False),
    'conjoint-over': (True, False),
    'copy': (True, False),
    'difference': (True, False),
    'disjoint-over': (True, False),
    'divide': (True, False),
    'exclusion': (True, False),
    'from': (True, False),
    'geometric': (True, False),
    'hard-light': (True, False),
    'hypot': (True, False),
    'in': (True, False),
    'mask': (True, True),
    'matte': (True, False),
    'max': (True, False),
    'min': (True, False),
    'minus': (True, False),
    'multiply': (True, False),
    'out': (True, False),
    'over': (True, True),
    'overlay': (True, False),
    'plus': (True, False),
    'screen': (True, False),
    'soft-light': (True, False),
    'stencil': (True, True),
    'under': (True, True),
    'xor': (True, False)
    }

import sys
# Import the core and GUI elements of Qt
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2 import QtWidgets
from PySide2 import QtCore

class MergeButton(QtWidgets.QLabel):
    def __init__(self, operation):
        super(MergeButton, self).__init__()

        self.operation = operation
        self.setText(operation)


        self.bgColor = '#525252'
        self.borderColor = '#000000'
        self.borderColor = '#959595'
        self.selectionColor = '#5285a6'
        self.setSelectionStatus(False)

        # set the border color to grey for buttons from an additional repository

        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setMouseTracking(True)
        self.setFixedWidth(105)
        self.setFixedHeight(35)

    def setSelectionStatus(self, selected = False):
        '''
        Define the style of the button for different states
        '''

        #if button becomes selected
        if selected:
            self.setStyleSheet("""
                                border: 1px solid black;
                                background:%s;
                                color:#eeeeee;
                                """%self.selectionColor)

        #if button becomes unselected
        else:
            self.setStyleSheet("""
                                border: 1px solid %s;
                                background:%s;
                                color:#eeeeee;
                                """%(self.borderColor, self.bgColor))

        self.selected = selected

    def enterEvent(self, event):
        '''
        Change color of the button when the mouse starts hovering over it
        '''
        self.setSelectionStatus(True)
        return True

    def leaveEvent(self,event):
        '''
        Change color of the button when the mouse stops hovering over it
        '''
        self.setSelectionStatus()
        return True


#

class MergeBox(QtWidgets.QWidget):
    def __init__(self):
        super(MergeBox, self).__init__()

        self.all_rows = QtWidgets.QVBoxLayout()
        self.setLayout(self.all_rows)

    def add_row(self):
        # Create a label widget with our text
        row = QtWidgets.QHBoxLayout()
        label = MergeButton('over')
        row.addWidget(label)
        self.all_rows.addLayout(row)

# Every Qt application must have one and only one QApplication object;
# it receives the command line arguments passed to the script, as they
# can be used to customize the application's appearance and behavior
qt_app = QtWidgets.QApplication(sys.argv)

# MergeBoxWindow = QtWidgets.QWidget()
# all_rows = QtWidgets.QVBoxLayout()
# MergeBoxWindow.setLayout(all_rows)
#
# # Create a label widget with our text
# row = QtWidgets.QHBoxLayout()
# label = MergeButton('over')
# row.addWidget(label)
# all_rows.addLayout(row)
#
# # Create a label widget with our text
# row = QtWidgets.QHBoxLayout()
# label = MergeButton('over')
# row.addWidget(label)
# all_rows.addLayout(row)


# Show it as a standalone widget
MergeBox = MergeBox()
MergeBox.add_row()
MergeBox.add_row()
MergeBox.show()

# Run the application's event loop
qt_app.exec_()