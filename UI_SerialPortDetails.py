from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

class UI_SerialPortDetails(QTreeWidget):
    def __init__(self, details):
        super().__init__()
        
        self.setColumnCount(2)
        self.setHeaderLabels(["Key", "Value"])
        
        items = []
        for key, values in details.items():
            item = QTreeWidgetItem([f'Port{key}'])
            for k, v in values.items():
                child = QTreeWidgetItem([k, v])
                item.addChild(child)
            items.append(item)

        self.insertTopLevelItems(0, items)
