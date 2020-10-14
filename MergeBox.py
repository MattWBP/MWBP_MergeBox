import sys
# Import the core and GUI elements of Qt
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

import queue
# import nuke

class MergeButton(QtWidgets.QLabel):
    def __init__(self, parent, operation):
        super(MergeButton, self).__init__()

        self.parent = parent
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

    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        self.parent.closeMergeBox()
        self.invoke()

    def command(self):
        node = nuke.createNode('Merge')
        node.knob('operation').setValue(self.operation)

    def invoke(self):
        # self.command()
        print(self.operation)

#

class MergeBox(QtWidgets.QWidget):
    def __init__(self):
        super(MergeBox, self).__init__()

        self.active = True

        self.setStyleSheet("background-color: rgba(0,0,0,0%)");

        self.all_rows = QtWidgets.QVBoxLayout()
        self.setLayout(self.all_rows)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shortcut = 'm'

        # define all the merge operations, if they're visible, if they're favourites.
        self.merge_operations = {
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

        self.q = queue.Queue()
        [self.q.put(i) for i in self.merge_operations]

        self.setup_layout()


    def add_row(self, count=0):
        # print('adding', count, 'items')
        row = QtWidgets.QHBoxLayout()
        row.setAlignment(QtCore.Qt.AlignCenter)
        for operation in range(count):
            operation = self.q.get()
            # print(operation)
            # Create a label widget with our text

            label = MergeButton(self, operation)
            row.addWidget(label)
        self.all_rows.addLayout(row)

    def add_centre_row(self, length=4):
        # print('adding centre row')
        row = QtWidgets.QHBoxLayout()
        row.setAlignment(QtCore.Qt.AlignCenter)
        for operation in range(int(length/2)):
            operation = self.q.get()
            label = MergeButton(self, operation)
            row.addWidget(label)

        spacer = QtWidgets.QLabel()
        spacer.setFixedWidth(105)
        spacer.setFixedHeight(35)
        spacer.setAlignment(QtCore.Qt.AlignCenter)
        spacer.setStyleSheet("background-color: rgba(255,0,0,0%)");
        row.addWidget(spacer)

        for operation in range(int(length/2)):
            operation = self.q.get()
            label = MergeButton(self, operation)
            row.addWidget(label)

        self.all_rows.addLayout(row)

    def setup_layout(self):
        self.add_row(1)
        self.add_row(2)
        self.add_row(4)
        self.add_row(5)
        self.add_centre_row(7)
        self.add_row(5)
        self.add_row(4)
        self.add_row(2)
        self.add_row(1)

    def showMergeBox(self):
        self.show()
        spawn = QtGui.QCursor().pos() - QtCore.QPoint((self.width()/2),(self.height()/2))
        self.move(spawn)

    def closeMergeBox(self):
        self.active = False
        # self.close()
        self.hide()

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return False

        if event.text() == self.shortcut:
            self.closeMergeBox()

            return True

    def keyPressEvent(self, event):
        if event.text() == self.shortcut:
            if event.isAutoRepeat():
                return False
        else:
            return False

    def eventFilter(self, object, event):
        if event.type() in [QtCore.QEvent.WindowDeactivate,QtCore.QEvent.FocusOut]:
            self.closeMergeBox()
            return True
        return False




def showMergeBox():
    global MergeBoxInstance


    # if not MergeBoxInstance and not MergeBoxInstance.active:
    if not MergeBoxInstance:
        MergeBoxInstance = MergeBox()
        MergeBoxInstance.show()
    elif not MergeBoxInstance.active():
        MergeBoxInstance = MergeBox()
        MergeBoxInstance.show()



MergeBoxInstance = None


# Every Qt application must have one and only one QApplication object;
# it receives the command line arguments passed to the script, as they
# can be used to customize the application's appearance and behavior
qt_app = QtWidgets.QApplication(sys.argv)

showMergeBox()


# Run the application's event loop
qt_app.exec_()