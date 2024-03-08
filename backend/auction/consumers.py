import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async




class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.auction_group_name = 'auction_room'
        await self.channel_layer.group_add(
            self.auction_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send_all_auctions_with_bids()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.auction_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            await self.save_bid(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    @sync_to_async
    def save_bid(self, data):
        from users.models import User
        from .models import Bid, Auction
        auction = Auction.objects.get(id=data['auction_id'])
        bidder = User.objects.get(id=data['bidder'])
        Bid.objects.create(
            amount=data['amount'],
            bidder=bidder,
            auction=auction
        )

    async def send_bid(self, event):
        await self.send(text_data=json.dumps(event))

    async def send_all_auctions_with_bids(self):
        auctions = await self.get_all_auctions_with_bids()
        await self.send(text_data=json.dumps({'all_auctions_with_bids': auctions}))

    @sync_to_async
    def get_all_auctions_with_bids(self):
        from .models import Bid, Auction
        auctions = Auction.objects.all()
        result = []
        for auction in auctions:
            bids = auction.bid_set.all()
            result.append({
                'id': auction.id,
                'vehicle': auction.content_object.name,
                'status': auction.status,
                'bids': [{'amount': float(bid.amount), 'bidder': bid.bidder.username} for bid in bids]
            })
        return result

    async def bid_message(self, event):
        # Handler for bid messages
        print("message received from group auction_room")
        print("event", event)
        await self.send(text_data=json.dumps(event))

    async def send_auction_countdown(self, event):
        from .models import Bid, Auction
        auction = await sync_to_async(Auction.objects.get)(id=event['auction_id'])
        await self.send(text_data=json.dumps({'countdown': auction.countdown}))
