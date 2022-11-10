from PySide6.QtWidgets import (
    QMainWindow,
)

from UI_SerialTerminal import UI_SerialTerminal
from SerialConnection import SerialConnection

def ps(thing_to_print=1):
        print(thing_to_print)

class SerialTerminal(UI_SerialTerminal):
    def __init__(self):
        super().__init__()
        
        self.ser = SerialConnection()
        self.port_combo.clear()
        self.port_combo.addItems(self.ser.available_ports)

        ps()

if __name__ == '__main__':
    from main import main
    main()