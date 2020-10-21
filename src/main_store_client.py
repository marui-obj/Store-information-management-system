#api testing
from store_client import WebSocketClient
import asyncio

async def main(my_client):
  while True :
    print("value : ",end ='')
    barcode = await my_client.get_barcode_list()  # read loop speed 0.1 sec (adjust in heartbeat method)
    print(barcode)
    await asyncio.sleep(2) # main loop speed (second unit)

client = WebSocketClient()
loop = asyncio.get_event_loop()
connection = loop.run_until_complete(client.connect())
tasks = [
    asyncio.ensure_future(client.heartbeat(connection)), 
    asyncio.ensure_future(client.receive_message(connection)),
    asyncio.ensure_future(main(client))
]
loop.run_until_complete(asyncio.wait(tasks))
