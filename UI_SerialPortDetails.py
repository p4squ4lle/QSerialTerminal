from PySide6.QtCore import QSize
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

DETAILS_WINDOW_MIN_SIZE = QSize(300, 250)

class UI_SerialPortDetails(QTreeWidget):
    def __init__(self, details):
        super().__init__()
        self.setWindowTitle('Details about available serial ports')
        self.setMinimumSize(DETAILS_WINDOW_MIN_SIZE)

        self.setColumnCount(2)
        self.setHeaderLabels(["Key", "Value"])
        
        items = []
        for key, values in details.items():
            item = QTreeWidgetItem([key])
            for k, v in values.items():
                if v:
                    child = QTreeWidgetItem([k, v])
                    item.addChild(child)
            items.append(item)

        self.insertTopLevelItems(0, items)
