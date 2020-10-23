# #api testing
from store_client import WebsocketClient
import asyncio

from PyQt5.QtWidgets import QApplication
# from PyQt5.QtCore import QEventLoop
# from asyncqt import QEventLoop
import sys

from gui import *

import time

async def main(my_client):
  while True :
   
    print("value : ",end ='')
    barcode = await my_client.get_barcode_list()  # read loop speed 0.1 sec (adjust in heartbeat method)
    print(barcode)
    await asyncio.sleep(2) # main loop speed (second unit)

def setup_pyqt():
 
  app = QApplication(sys.argv)
  scan_window = Main()
  sys.exit(app.exec())

def setup_websocket():

  client = WebsocketClient()
  loop = asyncio.get_event_loop()
  connection = loop.run_until_complete(client.connect())

  tasks = [
      asyncio.ensure_future(client.heartbeat(connection)), 
      asyncio.ensure_future(client.receive_message(connection)),
      asyncio.ensure_future(main(client))
  ]

  loop.run_until_complete(asyncio.wait(tasks))

if __name__ == "__main__":
  setup_websocket()
  
# if __name__ == "__main__":
#     import sys
#     import asyncio
#     from asyncqt import QEventLoop
#     # from asyncqt import QEventLoop
#     from PyQt5.QtWidgets import QApplication

#     app = QApplication(sys.argv)
#     loop = QEventLoop(app)
#     asyncio.set_event_loop(loop)
#     with loop:
        # scan_window = Main()

        # loop.run_until_complete(asyncio.wait(tasks))