from PySide6.QtCore import QSize, Qt, QEvent
from PySide6.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QMainWindow,
                               QPlainTextEdit, QPushButton, QVBoxLayout,
                               QWidget, QStatusBar)

# =============================================================================
# CONSTANTS
# =============================================================================
MAIN_WINDOW_TITLE = 'QSerialTerminal'
MAIN_WINDOW_MIN_SIZE = QSize(400, 300)

DEFAULT_BAUDRATES = ['9600', '19200', '115200']

class UI_SerialTerminal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(MAIN_WINDOW_TITLE)
        self.setMinimumSize(MAIN_WINDOW_MIN_SIZE)

        self.statusbar = QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.central_widget_layout = QVBoxLayout()
        self.port_baud_connect_layout = QVBoxLayout()
        self.port_baud_layout = QHBoxLayout()
        self.port_layout = QHBoxLayout()
        self.baud_layout = QHBoxLayout()

        self.port_label = QLabel('Port')
        self.port_combo = QComboBox()
        self.port_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.port_layout.addWidget(self.port_label)
        self.port_layout.addWidget(self.port_combo)

        self.baud_label = QLabel('Baudrate')
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(DEFAULT_BAUDRATES)
        self.baud_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.baud_layout.addWidget(self.baud_label)
        self.baud_layout.addWidget(self.baud_combo)

        self.port_baud_layout.addLayout(self.port_layout)
        self.port_baud_layout.addLayout(self.baud_layout)

        self.connect_layout = QHBoxLayout()
        self.connect_btn = QPushButton('Connect')
        self.disconnect_btn = QPushButton('Disconnect')
        self.disconnect_btn.setEnabled(True)

        self.connect_layout.addWidget(self.connect_btn)
        self.connect_layout.addWidget(self.disconnect_btn)

        self.port_baud_connect_layout.addLayout(self.port_baud_layout)
        self.port_baud_connect_layout.addLayout(self.connect_layout)

        self.cursor_line = 0
        self.cursor_col = 0
        self.terminal = QPlainTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.cursorPositionChanged.connect(
            self.on_cursor_position_changed
        )
        self.terminal.installEventFilter(self)
        self.terminal.viewport().installEventFilter(self)

        self.central_widget_layout.addLayout(self.port_baud_connect_layout)
        self.central_widget_layout.addWidget(self.terminal)


        self.central_widget = QWidget()
        self.central_widget.setLayout(self.central_widget_layout)

        self.setCentralWidget(self.central_widget)

    def on_cursor_position_changed(self):
        cursor = self.terminal.textCursor()
        self.cursor_col = cursor.columnNumber()
        self.cursor_line = cursor.blockNumber()
        line_col_string = f'({self.cursor_line}, {self.cursor_col})'
        self.statusbar.showMessage(line_col_string)
        
    def eventFilter(self, obj, event):
        if obj is self.terminal:
            if event.type() == QEvent.Type.KeyPress:
                if self.terminal.hasFocus():
                    if event.key() == Qt.Key.Key_Return:
                        self.on_enter_pressed()
                        return True
                    if event.key() == Qt.Key.Key_Backspace:
                        return self.on_backspace_pressed()
                    if event.key() == Qt.Key.Key_Up:
                        print('up key was pressed')
                        return True

        if event.type() in (QEvent.Type.MouseButtonDblClick,
                            QEvent.Type.MouseButtonPress,
                            QEvent.Type.MouseButtonRelease):
            if event.button() == Qt.MouseButton.LeftButton:
                return True

        return super().eventFilter(obj, event)

    def on_enter_pressed(self):
        self.terminal.setReadOnly(True)
        self.terminal.insertPlainText('\ncommand was sent')
        self.terminal.insertPlainText('\nthats the answer: yeah\n')
        self.terminal.setReadOnly(False)
        self.terminal.insertPlainText('>>> ')
        
    def on_backspace_pressed(self):
        if self.cursor_col < 5:
            return True
        return False


if __name__ == '__main__':
    from main import main
    main()