from PyQt5.QtWidgets import QDialog,QApplication
from PyQt5.QtCore import QThread
import sys
import websocket

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__()

        self.thread = ListenWebsocket()
        self.thread.start()



class ListenWebsocket(QThread):
    def __init__(self, parent=None):
        super(ListenWebsocket, self).__init__(parent)

        websocket.enableTrace(True)

        SERVER_IP = "localhost"
        SERVER_PORT = "5555"
        SERVER_URL = "ws://" + SERVER_IP + ":" + SERVER_PORT

        self.WS = websocket.WebSocketApp(SERVER_URL,
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close) 

    def run(self):
        #ws.on_open = on_open
        self.WS.run_forever()


    def on_message(self, ws, message):
        print (message)

    def on_error(self, ws, error):
        print (error)

    def on_close(self, ws):
        print ("### closed ###")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    QApplication.setQuitOnLastWindowClosed(False)

    window = Window()
    window.show()

    sys.exit(app.exec_())