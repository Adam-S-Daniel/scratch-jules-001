from typing import List, Dict, Any
from art_analysis_app.auction_tracker import AuctionItem
from art_analysis_app.market_analyzer import MarketAnalyzer

class OpportunityIdentifier:
    def __init__(self, analyzer: MarketAnalyzer, min_discount_threshold: float = 0.30):
        self.analyzer = analyzer
        self.min_discount_threshold = min_discount_threshold

    def find_opportunities(self, listings: List[AuctionItem]) -> List[Dict[str, Any]]:
        opportunities = []
        for listing in listings:
            if listing.estimated_price is None:
                continue

            expected_value = self.analyzer.calculate_expected_value(listing)
            if expected_value is not None and expected_value > 0:
                discount_amount = expected_value - listing.estimated_price
                discount_percentage = discount_amount / expected_value

                if discount_percentage >= self.min_discount_threshold:
                    opportunities.append({
                        "item": listing,
                        "expected_value": expected_value,
                        "discount_percentage": discount_percentage
                    })

        return opportunities
