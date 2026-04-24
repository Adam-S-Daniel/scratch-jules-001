from typing import Optional
from art_analysis_app.auction_tracker import AuctionTracker, AuctionItem

class MarketAnalyzer:
    def __init__(self, tracker: AuctionTracker):
        self.tracker = tracker

    def calculate_expected_value(self, listing: AuctionItem) -> Optional[float]:
        artist = listing.artist

        # Check if it's "School of"
        if artist.lower().startswith("school of "):
            famous_artist = artist[len("school of "):].strip()
            past_sales = [sale for sale in self.tracker.past_sales if sale.artist.lower() == famous_artist.lower()]
            multiplier = 0.10
        else:
            past_sales = [sale for sale in self.tracker.past_sales if sale.artist.lower() == artist.lower()]
            multiplier = 1.0

        if not past_sales:
            return None

        total_price = sum(sale.price for sale in past_sales if sale.price is not None)
        average_price = total_price / len(past_sales)

        return average_price * multiplier
