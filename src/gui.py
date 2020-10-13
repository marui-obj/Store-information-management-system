from PyQt5.QtWidgets import (QDialog, QListWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
                             QApplication, QInputDialog, QWidget, QMainWindow, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QIcon
import sys

class ScanWindow(QWidget):
    def __init__(self):

        # You can use "super().__init__()" instead
        super(ScanWindow, self).__init__()
        
        self.list = QListWidget() # Create scan list

        self.total = QLabel("0") # Create total money label
        self.total.setStyleSheet("background-color: lightgreen")
        
        vbox = QVBoxLayout() # Group widget in vertical box layout

        vbox.addWidget(self.total)

        for text, func in (("Add", self.add),
                           ("Edit", self.edit),
                           ("Remove", self.remove),
                           ("Checkout", self.checkout),
                           ("Return", self.returnToMain)
                           ):

            buttons = QPushButton(text)
            buttons.clicked.connect(func)

            vbox.addWidget(buttons)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.list)
        hbox.addLayout(vbox)
        self.setLayout(hbox)

        self.setWindowTitle("กับข้าวมาแล้วค๊าบบ")
        self.setWindowIcon(QIcon(".icon\\icon.png"))
        self.show()

    def add(self):
        ''' This function use for add item to cart list by manual '''

        row = self.list.currentRow()
        title = "Add item"
        message = "Enter BAR CODE"
        
        string, ok = QInputDialog.getText(self, title, message)

        if ok and string is not None and not string.isspace():
            self.list.insertItem(row, string)


    def edit(self):
        ''' This function use for edit item by manual '''

        print("Edit")

    def checkout(self):
        ''' This function use for checkout item by manual '''

        print("checkout")

    def remove(self):
        ''' This function use for remove item by manual '''

        row = self.list.currentRow()
        item = self.list.item(row)

        if item is None:
            return
        
        reply = QMessageBox.question(self, "Remove item", 
                                     "Remove {0} ?".format(str(item.text())),
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            item = self.list.takeItem(row)
            del item

    def returnToMain(self):

        self.new_window = Main()
        self.new_window.show()
        self.hide()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        for text, func in (("Scan", self.openScanWindow),
                           ("Data", self.openDataWindow)):
                           
            buttons = QPushButton(text)
            buttons.setSizePolicy(
                                    QSizePolicy.Preferred,
                                    QSizePolicy.Preferred
                                 )

            buttons.clicked.connect(func)

            layout.addWidget(buttons)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()
    def openScanWindow(self):

        self.new_window = ScanWindow()
        self.new_window.show()
        self.close()

    def openDataWindow(self):

        print("Data")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    scan_window = Main()
    sys.exit(app.exec())

        

        