import sys

from PySide6.QtWidgets import QApplication
from SerialTerminal import SerialTerminal

def main():
    app = QApplication(sys.argv)
    window = SerialTerminal()
    window.show()

    app.exec()

if __name__ == '__main__':
    main()
