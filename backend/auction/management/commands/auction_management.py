# yourapp/management/commands/auction_management.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from auction.models import Auction, Bid

class Command(BaseCommand):
    help = 'Automate auction status changes and check countdown'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        
        # Change status of auctions from open to running
        Auction.objects.filter(status='open', start_date__lte=now).update(status='running')
        
        # Change status of auctions from running to completed
        Auction.objects.filter(status='running', end_date__lte=now).update(status='completed')
        
        # Set won bid for the buyer with the highest bid amount
        auctions = Auction.objects.filter(status='completed', auctioned=False)
        for auction in auctions:
            highest_bid = auction.bid_set.order_by('-amount').first()
            if highest_bid:
                highest_bid.won = True
                highest_bid.save()
                auction.auctioned = True
                auction.save()

        # Check countdown for each auction and update if necessary
        auctions = Auction.objects.filter(status='running')
        for auction in auctions:
            if auction.countdown > 0:
                auction.countdown -= 1
                auction.save()
                if auction.countdown == 0 and auction.highest_bid.amount >= auction.vehicle.reserve_price:
                    # Set the highest bidder as the winner
                    highest_bidder = auction.highest_bid.bidder
                    auction.status = 'completed'
                    auction.buyer = highest_bidder
                    auction.auctioned = True
                    auction.save()
                    self.stdout.write(self.style.SUCCESS(f"Auction '{auction}' completed. Winner: {highest_bidder}"))
            elif auction.highest_bid.amount >= auction.vehicle.reserve_price:
                # If countdown is 0 and the highest bid is above reserve price, mark the buyer as the winner
                highest_bidder = auction.highest_bid.bidder
                auction.status = 'completed'
                auction.buyer = highest_bidder
                auction.auctioned = True
                auction.save()
                self.stdout.write(self.style.SUCCESS(f"Auction '{auction}' completed. Winner: {highest_bidder}"))

        self.stdout.write(self.style.SUCCESS('Auction automation completed successfully.'))
