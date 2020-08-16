from channels.consumer import SyncConsumer

class EchoConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Connect event is called")

        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print(event)
        self.send({
            'type': 'websocket.send',
            'text': event.get('text')
        })

    def websocket_disconnect(self, event):
        print("Connection is disconected")
        print(event)