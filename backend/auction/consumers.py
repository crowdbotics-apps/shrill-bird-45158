
from asgiref.sync import sync_to_async
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AuctionConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling auction events.
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

        # Send all auctions with their bids when connection is established
        await self.send_all_auctions_with_bids()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.auction_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receives a new bid from the WebSocket.
        """ 
        if text_data:
            try:
                text_data_json = json.loads(text_data)
                amount = text_data_json['amount']
                bidder = text_data_json['bidder']
                auction_id = text_data_json['auction_id']

                # Save the new bid to the database asynchronously
                await self.save_bid(amount, bidder, auction_id)

                # Send the new bid to the group
                # await self.channel_layer.group_send(
                #     self.auction_group_name,
                #     {
                #         'type': 'send_bid',
                #         'amount': amount,
                #         'bidder': bidder,
                #         'auction_id': auction_id
                #     }
                # )
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
        else:
            print("Received empty text_data.")

    @sync_to_async
    def save_bid(self, amount, bidder, auction_id):
        """
        Saves the new bid to the database.
        """
        from auction.models import Bid, Auction
        from users.models import User
        auction = Auction.objects.get(id=int(auction_id))
        Bid.objects.create(
            amount=amount,
            bidder=User.objects.get(id=int(bidder)),
            auction=auction
        )

    
    async def send_bid(self, event):
        """
        Handler method for sending a new bid to the WebSocket.
        """
        # Extract bid details from the event
        amount = event['amount']
        bidder = event['bidder']
        auction_id = event['auction_id']
        
        # Construct a message to send to the WebSocket
        message = {
            'type': 'bid_message',
            'amount': float(amount),
            'bidder': bidder,
            'auction_id': auction_id
        }
        
        # Send the message to the WebSocket
        await self.send(text_data=json.dumps(message))


    async def request_previous_bids(self, event):
        await self.send_all_bids(event)

    async def send_all_bids(self, event):
        """
        Sends all bids for a specific auction to the WebSocket.
        """
        from auction.models import Bid
        bids = await sync_to_async(Bid.objects.filter)(auction=event['auction_id'])
        all_bids = []
        for bid in bids:
            all_bids.append({
                'amount':float(bid.amount),
                'bidder': bid.bidder.username
            })
        await self.send(text_data=json.dumps({
            'all_bids': all_bids
        }))

    async def send_all_auctions(self, event):
        """
        Sends all auctions to the WebSocket.
        """
        from auction.models import Auction
        auctions = await sync_to_async(Auction.objects.all)()
        all_auctions = []
        for auction in auctions:
            all_auctions.append({
                'id': auction.id,
                'vehicle': auction.vehicle.name,
                'status': auction.status
            })
        await self.send(text_data=json.dumps({
            'all_auctions': all_auctions
        }))

    async def send_all_auctions_with_bids(self):
        """
        Sends all auctions with their bids to the WebSocket.
        """
        from auction.models import Auction, Bid
        all_auctions = await self.all_auction_with_bids()
        await self.send(text_data=json.dumps({
            'all_auctions_with_bids': all_auctions
        }))


    @sync_to_async
    def all_auction_with_bids(self):
        from auction.models import Auction, Bid
        auctions = Auction.objects.all()
        all_auctions = []
        for auction in auctions:
            auction_data = {
                'id': auction.id,
                'vehicle': auction.vehicle.name,
                'status': auction.status
            }
            bids = Bid.objects.filter(auction=auction)
            all_bids = []
            for bid in bids:
                all_bids.append({
                    'amount': float(bid.amount),
                    'bidder': bid.bidder.username
                })
            auction_data['bids'] = all_bids
            all_auctions.append(auction_data)
        return all_auctions

    async def send_auction_countdown(self, event):
        """
        Sends the auction countdown to the WebSocket.
        """
        from auction.models import Auction
        auction_id = event['auction_id']
        auction = await sync_to_async(Auction.objects.get)(id=auction_id)
        countdown = auction.countdown
        await self.send(text_data=json.dumps({
            'countdown': countdown
        }))

