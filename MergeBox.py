import sys
# Import the core and GUI elements of Qt
try:
    import nuke
    if nuke.NUKE_VERSION_MAJOR < 11:
        from PySide import QtCore, QtGui, QtGui as QtWidgets
    else:
        from PySide2 import QtGui, QtCore, QtWidgets
except:
    from PySide2 import QtWidgets
    from PySide2 import QtCore
    from PySide2 import QtGui

from pprint import pprint
import nuke


class MergeButton(QtWidgets.QLabel):
    merge_selected = QtCore.Signal(str)
    def __init__(self, operation, ):
        super(MergeButton, self).__init__()

        # arguments
        self.operation = operation
        self.setText(operation)
        
        # variables
        self.positon = (0,0)

        # ui
        self.bgColor = '#525252'
        self.borderColor = '#000000'
        self.borderColor = '#959595'
        self.selectionColor = '#5285a6'
        self.setSelectionStatus(False)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setMouseTracking(True)
        self.setFixedWidth(105)
        self.setFixedHeight(35)
        
    def setSelectionStatus(self, selected = False):
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
        self.setSelectionStatus(True)
        return True

    def leaveEvent(self,event):
        self.setSelectionStatus()
        return True


    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        # self.parent().custom_slot(self.operation)
        self.merge_selected.emit(self.text())


class MergeBox(QtWidgets.QWidget):
    # signals

    def __init__(self):
        super(MergeBox, self).__init__()

        # self.merge_select.connect(self.custom_slot)

        # layout
        self.all_rows = QtWidgets.QVBoxLayout()
        self.setLayout(self.all_rows)

        # style
        self.setStyleSheet("background-color: rgba(0,0,0,0%)")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # variables
        self.active = True
        self.shortcut = 'm'

        # define all the merge operations, if they're visible, if they're favourites.
        self.merge_operations = {
            'average':       (1,1),

            'atop':          (2,1),
            'color-burn':    (2,2),

            'color-dodge':   (3,1),
            'conjoint-over': (3,2),
            'copy':          (3,3),
            'difference':    (3,4),

            'disjoint-over': (4,1),
            'divide':        (4,2),
            'exclusion':     (4,3),
            'from':          (4,4),
            'geometric':     (4,5),

            'hard-light':    (5,1),
            'hypot':         (5,2),
            'in':            (5,3),
            # center
            'mask':          (5,4),
            'matte':         (5,5),
            'max':           (5,6),

            'min':           (6,1),
            'minus':         (6,2),
            'multiply':      (6,3),
            'out':           (6,4),
            'over':          (6,5),

            'overlay':       (7,1),
            'plus':          (7,2),
            'screen':        (7,3),
            'soft-light':    (7,4),

            'stencil':       (8,1),
            'under':         (8,2),

            'xor':           (9,1)
        }

        self.setup_ui()

    def merge_selected_slot(self, operation):
        self.hide()
        self.create_node(operation)
        self.close()

    def create_node(self, operation):
        # node = nuke.createNode('Merge')
        # node.knob('operation').setValue(operation)
        print('creating node:', operation)

    def setup_ui(self):
        row_count = max(self.merge_operations.values())[0]
        center_row = (row_count - 1)/2 +1


        for row in range(1,row_count+1):
            this_row = row
            this_row_operations = [k for k,v in self.merge_operations.items() if v[0]==this_row]
            this_row_operations_ordered = {}

            for row_operation in this_row_operations:
                operation = row_operation
                row, position = self.merge_operations[operation]
                this_row_operations_ordered[position] = row_operation

            # pprint(this_row_operations_ordered)

            row_layout = QtWidgets.QHBoxLayout()
            row_layout.setAlignment(QtCore.Qt.AlignCenter)

            if this_row == center_row:          
                center_count = int(len(this_row_operations_ordered)/2)
            else:
                center_count = None

            for count in this_row_operations_ordered:
                label = MergeButton(this_row_operations_ordered[count])
                label.merge_selected.connect(self.merge_selected_slot)
                row_layout.addWidget(label)

                if center_count:
                    if count == center_count:
                        spacer = QtWidgets.QLabel()
                        spacer.setFixedWidth(105)
                        spacer.setFixedHeight(35)
                        spacer.setAlignment(QtCore.Qt.AlignCenter)
                        spacer.setStyleSheet("background-color: rgba(255,0,0,0%)")
                        row_layout.addWidget(spacer)

            self.all_rows.addLayout(row_layout)

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