from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QComboBox,
    QPushButton,
    QPlainTextEdit,
)

# =============================================================================
# CONSTANTS
# =============================================================================
MAIN_WINDOW_TITLE = 'QSerialTerminal'
MAIN_WINDOW_MIN_SIZE = QSize(400, 300)

class UI_SerialTerminal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(MAIN_WINDOW_TITLE)
        self.setMinimumSize(MAIN_WINDOW_MIN_SIZE)

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
        self.baud_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.baud_layout.addWidget(self.baud_label)
        self.baud_layout.addWidget(self.baud_combo)

        self.port_baud_layout.addLayout(self.port_layout)
        self.port_baud_layout.addLayout(self.baud_layout)

        self.connect_layout = QHBoxLayout()
        self.connect_btn = QPushButton('Connect')
        self.disconnect_btn = QPushButton('Disconnect')
        self.connect_layout.addWidget(self.connect_btn)
        self.connect_layout.addWidget(self.disconnect_btn)

        self.port_baud_connect_layout.addLayout(self.port_baud_layout)
        self.port_baud_connect_layout.addLayout(self.connect_layout)

        self.terminal = QPlainTextEdit()
        self.central_widget_layout.addLayout(self.port_baud_connect_layout)
        self.central_widget_layout.addWidget(self.terminal)


        self.central_widget = QWidget()
        self.central_widget.setLayout(self.central_widget_layout)

        self.setCentralWidget(self.central_widget)


if __name__ == '__main__':
    from main import main
    main()