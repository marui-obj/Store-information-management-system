from PyQt5.QtWidgets import (QDialog, QListWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
                             QApplication, QInputDialog, QWidget, QMainWindow, QSizePolicy, QMessageBox)

from PyQt5.QtGui import QIcon

from database import Command

from ItemManager import Cart

import sys


class ScanWindow(QWidget):
    def __init__(self):

        self.cart = Cart()        
        self.total_price = 0
        
        self.barcode_dict = {}

        self.database = Command() # connect to database

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

        self.setWindowTitle("Scan mode")
        self.setWindowIcon(QIcon(".icon\\icon.png"))
        self.show()

    def add(self):
        ''' This function use for add item to cart list by manual '''

        row = self.list.currentRow()

        title = "Add item"
        message = "Enter BAR CODE"
        barcode, ok_barcode = QInputDialog.getText(self, title, message)

        item = self.database.getItem(barcode)

        if self.cart.isExist(barcode):
            print(barcode, "Already exist")
            return

        if ok_barcode and item:
            title = "Quality"
            message = "Enter quality"
            quality, ok_quality = QInputDialog.getText(self, title, message)

            if ok_quality and quality is not None and not quality.isspace() and not quality == "":

                item_name, item_price, item_type = item
                string_item = "{0}; {1} จำนวน : {2} ราคา : {3}".format(barcode, item_name, quality, item_price)

                self.cart.addItem(barcode, item_name, item_price, item_type, quality)

                self.update_price()

                self.list.insertItem(row, string_item)

                print(self.list.item(row))


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
            self.cart.remove(self.getQrInDisplay(item))
            del item
            self.update_price()



    def returnToMain(self):

        self.new_window = Main()
        self.new_window.show()
        self.hide()

    def update_price(self):
        self.total_price = self.cart.getCartPrice()
        self.total.setText(str(self.total_price))

    def getQrInDisplay(self, item):
        string = item.text()
        barcode = ""
        for char in string:
            if char == ';':
                break
            barcode += char
        return barcode


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
        return self.new_window

    def openDataWindow(self):

        print("Data")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    scan_window = Main()
    sys.exit(app.exec())

        

        