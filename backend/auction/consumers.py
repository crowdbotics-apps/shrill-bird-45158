# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AuctionConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling auction events.

    This consumer connects to the WebSocket and adds itself to the auction group.
    It handles receiving new bids and sending bid messages to the group.
    """

    async def connect(self):
        """
        Connects the consumer to the WebSocket and adds it to the auction group.
        """
        self.auction_group_name = 'auction_room'
        await self.channel_layer.group_add(
            self.auction_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.auction_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
            """
            Receives text data from the WebSocket connection and handles it accordingly.
            
            Args:
                text_data (str): The text data received from the WebSocket connection.
            """
            data = json.loads(text_data)
            if 'new_bid' in data:
                # Handle new bid
                
                await self.channel_layer.group_send(
                    self.auction_group_name,
                    {
                        'type': 'bid_message',
                        'new_bid': data['new_bid']
                    }
                )

    async def bid_message(self, event):
            """
            Sends a bid message to the client.

            Args:
                event (dict): The event containing the new bid.

            Returns:
                None
            """
            new_bid = event['new_bid']
            await self.send(text_data=json.dumps({
                'new_bid': new_bid
            }))

    async def send_bidding_status(self, event):
            """
            Sends the bidding status to the client.

            Args:
                event (dict): The event containing the bidding status.

            Returns:
                None
            """
            bidding_status = event['bidding_status']
            await self.send(text_data=json.dumps({
                'bidding_status': bidding_status
            }))
