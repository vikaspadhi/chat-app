from channels.consumer import SyncConsumer , AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json
from asgiref.sync import async_to_sync
from .models import Chat,Group

class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self,event):
        print("websocket connected...")
        print("Channel Layer - ",self.channel_layer)
        print("Channel Name - ",self.channel_name)
        
        self.grp_name = self.scope['url_route']['kwargs']['groupname']

        # group_add function is async to make it work in syncConsumer we have to use async_to_sync

        # adding channel into default group
        async_to_sync(self.channel_layer.group_add)(self.grp_name,self.channel_name)

        #accepting the connection
        self.send({'type':'websocket.accept'})

    def websocket_receive(self,event):
        # print("Message received...",event['text'])
        data = json.loads(event['text'])
        msg=data['msg']

        group = Group.objects.get(name=self.grp_name)

        chat = Chat(msg=msg,group = group)
        chat.save()

        async_to_sync(self.channel_layer.group_send)(self.grp_name,{
            'type':'chat.message',
            'message':event['text']
        })

    def chat_message(self,event):
        self.send({
            'type':'websocket.send',
            'text': event['message']
        })       

    def websocket_disconnect(self,event):
        print("websocket disconnected...")

        # removing channel from group when disconnected
        async_to_sync(self.channel_layer.group_discard)(self.grp_name,self.channel_name)
        raise StopConsumer


class MyAsyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self,event):
        print("websocket connected...")
        print("Channel Layer - ",self.channel_layer)
        print("Channel Name - ",self.channel_name)
        await self.send({'type':'websocket.accept'})

    async def websocket_receive(self,event):
        print("Message received...")
        print(event['text'])
        for i in range(20):
            data = {'count':i}
            await self.send({'type':'websocket.send','text':json.dumps(data)})
            await asyncio.sleep(1)

    async def websocket_disconnect(self,event):
        print("websocket disconnected...")
        raise StopConsumer
