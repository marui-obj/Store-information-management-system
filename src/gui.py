import sys

from PyQt5 import QtCore, QtWebSockets, QtNetwork
from PyQt5.QtCore import QUrl, QCoreApplication, QTimer,pyqtSlot,Qt
import json

from PyQt5.QtWidgets import (QDialog, QListWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
                             QApplication, QInputDialog, QWidget, QMainWindow, QSizePolicy, QMessageBox)

from PyQt5.QtGui import QIcon

from database import Command


from ItemManager import Cart

import sys


class ScanWindow(QWidget):
    def __init__(self,parent = None):
        ################################# Back - End ##############################
        super().__init__(parent)
        IP = "127.0.0.1"
        PORT = "1302"
        URL = "ws://127.0.0.1:1302"
        

        self.client =  QtWebSockets.QWebSocket("",QtWebSockets.QWebSocketProtocol.Version13,None)
        
   
        
        self.client.textMessageReceived.connect(self.auto_add)
        # self.client.disconnected.connect(self.socketDisconnected)



        self.client.error.connect(self.error)

        self.client.open(QUrl(URL))
        self.client.pong.connect(self.onPong)

        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.send_message)
        
        self.timer2.setInterval(1000)
        self.timer2.start()
        
        



        ################################## Front - End ########################

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

        for text, func in (("Add", self.manual_add),
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

    ################################# Back - End ##############################
    def quit_app(self):
        print("timer timeout - exiting 55")
        QCoreApplication.quit()
        
    def findItemFromBarcode(self,barcode):
        for item in self.list.findItems("", Qt.MatchContains) :
            barcode_search = item.text().split(';')[0]
            if (barcode == barcode_search):
                return item


    def auto_add(self, message):
        
        data = json.loads(message)
        
        barcode = data["barcode"]
        if barcode:
            print("client receive - message: {}".format(message))

            if self.cart.isExist(barcode):

                current_item = self.cart.getItemByBarCode(barcode)
                name = current_item.item_name
                price = current_item.item_price
                
                item = self.findItemFromBarcode(barcode)

                quantity = self.cart.updateQuantity(current_item)  
                item.setText("{0}; {1} จำนวน : {2} ราคา : {3}".format(barcode, name, quantity, price))
                self.update_price()
               
    
            else:
                self.add_item(barcode)
         

    def do_ping(self):
        print("client: do_ping")
        self.client.ping(b"foo")

    @pyqtSlot()
    def send_message(self):
        # print("client: send_message")
        self.client.sendTextMessage(json.dumps({"request" : 1}))

    def onPong(self, elapsedTime, payload):
        print("onPong - time: {} ; payload: {}".format(elapsedTime, payload))

    def error(self, error_code):
        print("error code: {}".format(error_code))
        print(self.client.errorString())

    def close(self):
        self.client.close()

    
    ################################## Front - End ########################
    def manual_add(self):
        ''' This function use for add item to cart list by manual '''

        title = "Add item"
        message = "Enter BAR CODE"
        barcode, ok_barcode = QInputDialog.getText(self, title, message)
        title = "Quality"
        message = "Enter quality"
        quality, ok_quality = QInputDialog.getText(self, title, message)

        self.add_item(barcode,ok_barcode,quality, ok_quality)

        

    def add_item(self, barcode,ok_barcode=True,quality= '1',ok_quality=True):
       
        item = self.database.getItem(barcode)
        row = self.list.currentRow()
        if barcode :
            if self.cart.isExist(barcode):
                print(barcode, "Already exist")
                return

            if ok_barcode and item:

                if ok_quality and quality is not None and not quality.isspace() and not quality == "":

                    item_name, item_price, item_type = item
                    string_item = "{0}; {1} จำนวน : {2} ราคา : {3}".format(barcode,item_name, quality, item_price)

                    self.cart.addItem(barcode, item_name, item_price, item_type, quality)

                    self.update_price()

                    self.list.insertItem(row, string_item)

                    print(self.list.item(row))


    def edit(self):
        row = self.list.currentRow()
        item = self.list.item(row)
        ##
        # lst = [i.text() ]
        # for i in self.list.findItems("", Qt.MatchContains) :
        #     barcode = i.text().split(';')[0]
            
        # print(lst)
       
        ##
        barcode = self.getBCodeInDisplay(item)

        current_item = self.cart.getItemByBarCode(barcode)

        title = "Edit quantity"
        message = "Enter new quantity at {0}".format(current_item.getName())

        quantity, ok = QInputDialog.getText(self, title, message)

        if ok and quantity is not None and not quantity.isspace() and not quantity == "":
            name = current_item.item_name
            price = current_item.item_price
            item.setText("{0}; {1} จำนวน : {2} ราคา : {3}".format(barcode, name, quantity, price))
            self.cart.editQuantity(current_item, quantity)
            self.update_price()



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
            self.cart.remove(self.getBCodeInDisplay(item))
            del item
            self.update_price()



    def returnToMain(self):

        self.new_window = Main()
        self.new_window.show()
        self.hide()

    def update_price(self):
        self.total_price = self.cart.getCartPrice()
        self.total.setText(str(self.total_price))

    def getBCodeInDisplay(self, item):
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


if __name__ == '__main__':

    app = QApplication(sys.argv)

    scan_window = Main()
    sys.exit(app.exec())

    app.exec_()

        

        