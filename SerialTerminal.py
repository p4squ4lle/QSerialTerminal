from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
)

from UI_SerialTerminal import UI_SerialTerminal
from SerialConnection import SerialConnection

SERIAL_TIMEOUT = 1    # [seconds]
DEFAULT_BAUDRATES = ['9600', '19200', '115200']

def ps(thing_to_print=1):
        print(thing_to_print)

class SerialTerminal(UI_SerialTerminal):
    def __init__(self):
        super().__init__()
        
        self.ser = SerialConnection()
        self.port_combo.clear()
        self.port_combo.addItems(self.ser.available_ports)

        self.connect_btn.clicked.connect(self.on_connect_btn_clicked)
        self.disconnect_btn.clicked.connect(self.on_disconnect_btn_clicked)

        

    def on_connect_btn_clicked(self):
        if not self.ser.connected:
            self.connect_btn.setText("...")
            self.port = self.port_combo.currentData(0)
            self.baudrate = int(self.baud_combo.currentData(0))
            self.timeout = SERIAL_TIMEOUT
            self.ser.connect(self.port, self.baudrate, self.timeout)
            self.disconnect_btn.setEnabled(True)
            self.connect_btn.setEnabled(False)
            self.connect_btn.setText("connect")

            self.terminal.setReadOnly(False)
            self.terminal.setFocus()
            self.terminal.insertPlainText('>>> ')

    def on_disconnect_btn_clicked(self):
        self.ser.close()
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)

        self.terminal.setReadOnly(True)

if __name__ == '__main__':
    from main import main
    main()