import websockets
import asyncio
import json 

class WebSocketClient():

    def __init__(self):
        self.barcode_list = []

    def json_massage(self,message):
        '''
        request to server to get barcode value in json pattern   
        '''
        return json.dumps({"client" : message,"request" : 1})

    
    async def get_barcode_list(self):
        '''
         Return barcode value in list type
        '''
        return self.barcode_list

    async def connect(self):
        '''
            Connecting to websocket server
            websockets.client.connect returns a WebSocketClientProtocol, which is used to send and receive messages
        '''

        # SERVER_IP = "192.168.1.50"
        SERVER_IP = "localhost"
        SERVER_PORT = "5555"
        SERVER_URL = "ws://" + SERVER_IP + ":" + SERVER_PORT
        

        self.connection = await websockets.client.connect(SERVER_URL)
        if self.connection.open:
            print('Connection stablished. Client correcly connected')
            
            # Send greeting
            message = self.json_massage("start client")
            await self.send_message(message)
            return self.connection


    async def send_message(self, message):
        '''
            Sending message to websocket server
        '''
        await self.connection.send(message)

    async def receive_message(self, connection):
        '''
            Receiving all server messages and handling them
        '''
        while True:
            try:
                async for message in connection:
                    data = json.loads(message)
                    if(data['barcode'] != "" ):
                       self.barcode_list.append(data["barcode"])
                        
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break
            

    async def heartbeat(self, connection):
        '''
        Sending heartbeat to server every 5 seconds
        Ping - pong messages to verify connection is alive
        '''
        while True:
            try:
                ping = self.json_massage("ping")
                await connection.send(ping)
                await asyncio.sleep(0.1)
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break
          

if __name__ == '__main__':
    client = WebSocketClient()
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(client.connect())
    tasks = [
        asyncio.ensure_future(client.heartbeat(connection)),
        asyncio.ensure_future(client.receive_message(connection)),

    ]

    loop.run_until_complete(asyncio.wait(tasks))