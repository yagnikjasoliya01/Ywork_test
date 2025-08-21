import json
from channels.generic.websocket import AsyncWebsocketConsumer
from motor.motor_asyncio import AsyncIOMotorClient

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.department_id = self.scope['url_route']['kwargs']['department_id']
        self.room_group_name = f'chat_{self.department_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Connect to MongoDB
        self.mongo_client = AsyncIOMotorClient('mongodb://localhost:27017/') # Replace with your MongoDB host
        self.db = self.mongo_client['company_chat']
        self.collection = self.db['messages']
        
        await self.accept()

        # Retrieve and send chat history on connect
        async for message in self.collection.find({'group_name': self.room_group_name}).sort([('timestamp', 1)]):
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message['message'],
                'username': message['username'],
                'timestamp': str(message['timestamp']),
            }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Close MongoDB connection
        self.mongo_client.close()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        # Save message to MongoDB
        await self.collection.insert_one({
            'group_name': self.room_group_name,
            'username': username,
            'message': message,
            'timestamp': json.loads(self.scope['url_route']['kwargs']['department_id']) # Using a placeholder for now
        })

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'username': username
        }))