from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QTextCursor

from UI_SerialTerminal import UI_SerialTerminal
from SerialConnection import SerialConnection

SERIAL_TIMEOUT = 1    # [seconds]

CYCLE_COMMANDS_KEYS = [Qt.Key.Key_Up, Qt.Key.Key_Down]

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
        self.terminal_command_idx = 0
        


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
        self.terminal.insertPlainText('\n')
        self.terminal.setReadOnly(True)

    def eventFilter(self, obj, event):
        if obj is self.terminal and self.terminal.hasFocus():
            if event.type() == QEvent.Type.KeyPress:
                key = event.key()
                if key == Qt.Key.Key_Return:
                    self.on_enter_pressed()
                    return True
                if key in CYCLE_COMMANDS_KEYS:
                    if key == Qt.Key.Key_Up:
                        self.terminal_command_idx -= 1
                        self.terminal_command_idx = max(
                            -len(self.ser.last_commands), 
                            self.terminal_command_idx
                        )
                    if key == Qt.Key.Key_Down:
                        self.terminal_command_idx += 1
                        self.terminal_command_idx = min(
                            0, self.terminal_command_idx
                        )
                    return self.cycle_commands()

        return super().eventFilter(obj, event)

    def on_enter_pressed(self):
        self.terminal_command_idx = 0

        terminal_text = self.terminal.toPlainText()
        current_command = terminal_text.split('>>> ')[-1]
        print(current_command)
        terminal_cursor = self.terminal.textCursor()
        terminal_cursor.movePosition(QTextCursor.End)
        self.terminal.setTextCursor(terminal_cursor)
        self.terminal.setReadOnly(True)
        
        self.ser.send_string(current_command)
        self.ser.read_string()
        current_answer = self.ser.last_messages[-1]

        self.terminal.insertPlainText(f'\n{current_answer}\r')
        self.terminal.setReadOnly(False)
        self.terminal.insertPlainText('>>> ')
        self.terminal.ensureCursorVisible()       
    
    def cycle_commands(self):
        terminal_text = self.terminal.toPlainText()
        text_upto_command = '>>> '.join(terminal_text.split('>>> ')[:-1])
        self.terminal.clear()
        self.terminal.insertPlainText(text_upto_command)
        self.terminal.insertPlainText('>>> ')
        if self.terminal_command_idx<0:
            self.terminal.insertPlainText(
            self.ser.last_commands[self.terminal_command_idx]
        )
        self.terminal.ensureCursorVisible()
        return True

if __name__ == '__main__':
    from main import main
    main()