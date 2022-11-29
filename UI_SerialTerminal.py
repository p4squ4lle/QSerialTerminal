from PySide6.QtCore import QSize, Qt, QEvent
from PySide6.QtGui import QKeySequence, QAction, QIcon, QPixmap
from PySide6.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QMainWindow,
                               QPlainTextEdit, QPushButton, QVBoxLayout,
                               QWidget, QStatusBar, QToolBar)


# =============================================================================
# CONSTANTS
# =============================================================================
MAIN_WINDOW_TITLE = 'QSerTer'
MAIN_WINDOW_MIN_SIZE = QSize(400, 300)

DEFAULT_BAUDRATES = ['9600', '19200', '115200']

KEYS_TO_BYPASS = [Qt.Key.Key_PageUp,
                  Qt.Key.Key_PageDown,
                  Qt.Key.Key_Home,
                  Qt.Key.Key_End]

TOOLBAR_LABEL_PADDING = 5    # [pixel]

class UI_SerialTerminal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(MAIN_WINDOW_TITLE)
        self.setMinimumSize(MAIN_WINDOW_MIN_SIZE)
        self.setWindowIcon(QIcon('./resources/icons/rs232.jpg'))

        self.central_widget = QWidget()

        # =====================================================================
        # Toolbar
        # =====================================================================
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.toggleViewAction().setVisible(False)

        self.port_lbl = QLabel('Port')
        self.port_lbl.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.port_lbl.setStyleSheet(f'padding :{TOOLBAR_LABEL_PADDING}px')
        self.toolbar.addWidget(self.port_lbl)
        self.port_dropdown = QComboBox()
        self.port_dropdown.setStatusTip('Select serial port')
        self.toolbar.addWidget(self.port_dropdown)

        self.refresh_action = QAction(QIcon('./resources/icons/refresh.jpg'), 'Refresh button', self)
        self.refresh_action.setStatusTip('Refresh serial port list')
        self.toolbar.addAction(self.refresh_action)

        self.baud_lbl = QLabel('Baudrate')
        self.baud_lbl.setStyleSheet(f'padding :{TOOLBAR_LABEL_PADDING}px')
        self.toolbar.addWidget(self.baud_lbl)
        self.baud_dropdown = QComboBox()
        self.baud_dropdown.setStatusTip(
            'Select baudrate for serial connection'
        )
        self.baud_dropdown.addItems(DEFAULT_BAUDRATES)
        self.baud_dropdown.setCurrentIndex(2)
        self.toolbar.addWidget(self.baud_dropdown)
        
        self.connect_action = QAction('>>>', self)
        self.connect_action.setStatusTip('Establish serial connection')
        self.toolbar.addAction(self.connect_action)

        self.disconnect_action = QAction('<<X', self)
        self.disconnect_action.setStatusTip('Close serial connection')
        self.disconnect_action.setEnabled(False)
        self.toolbar.addAction(self.disconnect_action)

        self.details_action = QAction('ooo', self)
        self.details_action.setStatusTip('Show details about available ports')
        self.toolbar.addAction(self.details_action)

        self.addToolBar(self.toolbar)

        # =====================================================================
        # Statusbar
        # =====================================================================
        self.statusbar = QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        # =====================================================================
        # Menubar
        # =====================================================================
        

        # =====================================================================
        # Port Combo and Baudrate Combo
        # =====================================================================
        # self.port_label = QLabel('Port')
        # self.port_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        # self.port_combo = QComboBox()
        
        # self.baud_label = QLabel('Baudrate')
        # self.baud_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        # self.baud_combo = QComboBox()
        # self.baud_combo.addItems(DEFAULT_BAUDRATES)
        # self.baud_combo.setCurrentIndex(2)
        
        # =====================================================================
        # Connect, Disconnect, Refresh and Details Buttons
        # =====================================================================
        # self.connect_btn = QPushButton('Connect')
        # self.disconnect_btn = QPushButton('Disconnect')
        # self.disconnect_btn.setEnabled(False)
        # self.refresh_btn = QPushButton('Refresh')
        # self.details_btn = QPushButton('Details...')

        # =====================================================================
        # Terminal UI
        # =====================================================================
        self.cursor_line = 0
        self.cursor_col = 0
        self.terminal = QPlainTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setContentsMargins(0,0,0,0)
        self.terminal.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.terminal.cursorPositionChanged.connect(
            self.on_cursor_position_changed
        )
        self.terminal.installEventFilter(self)
        self.terminal.viewport().installEventFilter(self)

        # =====================================================================
        # Layout
        # =====================================================================   
        # self.port_layout = QHBoxLayout()
        # self.port_layout.addWidget(self.port_label)
        # self.port_layout.addWidget(self.port_combo)

        # self.baud_layout = QHBoxLayout()
        # self.baud_layout.addWidget(self.baud_label)
        # self.baud_layout.addWidget(self.baud_combo)

        # self.port_baud_layout = QHBoxLayout()
        # self.port_baud_layout.addLayout(self.port_layout)
        # self.port_baud_layout.addLayout(self.baud_layout)

        # self.connect_layout = QHBoxLayout()
        # self.connect_layout.addWidget(self.connect_btn)
        # self.connect_layout.addWidget(self.disconnect_btn)
        # self.connect_layout.addWidget(self.refresh_btn)
        # self.connect_layout.addWidget(self.details_btn)

        # self.port_baud_connect_layout = QVBoxLayout()
        # self.port_baud_connect_layout.addLayout(self.port_baud_layout)
        # self.port_baud_connect_layout.addLayout(self.connect_layout)

        self.central_widget_layout = QVBoxLayout()
        self.central_widget_layout.setContentsMargins(0,0,0,0)
        # self.central_widget_layout.addLayout(self.port_baud_connect_layout)
        self.central_widget_layout.addWidget(self.terminal)

        self.central_widget.setLayout(self.central_widget_layout)
        self.setCentralWidget(self.central_widget)

        self.update_stylesheet(
            css='QPlainTextEdit {color: rgb(15,255,15)}'
        )

    def on_cursor_position_changed(self):
        cursor = self.terminal.textCursor()
        self.cursor_col = cursor.columnNumber()
        self.cursor_line = cursor.blockNumber()
        line_col_string = f'({self.cursor_line}, {self.cursor_col})'
        self.statusbar.showMessage(line_col_string)
        
    def eventFilter(self, obj, event):
        if obj is self.terminal and self.terminal.hasFocus():
            if event.type() == QEvent.Type.KeyPress:
                if event.key() in KEYS_TO_BYPASS:
                    return True
                if event.key() == Qt.Key.Key_Backspace:
                    return self.on_backspace_pressed()
                if event.key() == Qt.Key.Key_Left:
                    return self.on_backspace_pressed()
                if event.key() == Qt.Key.Key_Right:
                    return False
                if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                    modifier = 'Ctrl+'
                    key = QKeySequence(event.key()).toString()
                    print(modifier+key)
                    if key=='V' or key=='C':
                        return False
                    return True

        if event.type() in (QEvent.Type.MouseButtonDblClick,
                            QEvent.Type.MouseButtonPress,
                            QEvent.Type.MouseButtonRelease):
            if event.button() == Qt.MouseButton.LeftButton:
                return True

        return super().eventFilter(obj, event)
        
    def on_backspace_pressed(self):
        if self.cursor_col < 5:
            return True
        return False

    def update_stylesheet(self, css):
        self.setStyleSheet(css)

if __name__ == '__main__':
    from main import main
    main()