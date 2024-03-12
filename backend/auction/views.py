# views.py
from django.shortcuts import render
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

def update_bidding_status(request):
    # Your logic to fetch bidding status from the database
    
    
    bidding_status = {
        'current_bid': current_bid,
        'highest_bidder': highest_bidder,
        # Add more relevant information as needed
    }

    # Send the bidding status to all connected clients
    async_to_sync(channel_layer.group_send)(
        'auction_room',
        {
            'type': 'send_bidding_status',
            'bidding_status': bidding_status
        }
    )

    return JsonResponse({'status': 'success'})
