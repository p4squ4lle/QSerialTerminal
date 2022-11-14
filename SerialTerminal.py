from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
)

from UI_SerialTerminal import UI_SerialTerminal
from SerialConnection import SerialConnection

SERIAL_TIMEOUT = 1    # [seconds]


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

        self.terminal.installEventFilter(self)


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

    def eventFilter(self, obj, event):
        if obj is self.terminal and self.terminal.hasFocus():
            if event.type() == QEvent.Type.KeyPress:
                if event.key() == Qt.Key.Key_Return:
                    self.on_enter_pressed()
                    return True
                if event.key() == Qt.Key.Key_Up:
                    print('up key was pressed')
                    return True
                if event.key() == Qt.Key.Key_Down:
                    print('down key was pressed')
                    return True

        return super().eventFilter(obj, event)

    def on_enter_pressed(self):
        terminal_text = self.terminal.toPlainText()
        current_command = terminal_text.split('\n')[-1][4:]
        self.terminal.setReadOnly(True)
        self.terminal.insertPlainText('\nCommand: ')
        self.terminal.insertPlainText(current_command)
        self.ser.send_string(current_command)
        self.ser.read_string()
        current_answer = self.ser.last_messages[-1]
        self.terminal.insertPlainText('\nthats the answer: ')
        self.terminal.insertPlainText(current_answer)
        self.terminal.setReadOnly(False)
        self.terminal.insertPlainText('\n>>> ')

if __name__ == '__main__':
    from main import main
    main()