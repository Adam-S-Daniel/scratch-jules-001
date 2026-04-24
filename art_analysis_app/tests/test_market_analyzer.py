import pytest
from art_analysis_app.auction_tracker import AuctionItem, AuctionTracker
from art_analysis_app.market_analyzer import MarketAnalyzer

def test_calculate_expected_value_exact_artist():
    tracker = AuctionTracker()
    tracker.add_past_sale(AuctionItem(id="1", artist="Artist A", title="Work 1", price=1000, region="mid-Atlantic"))
    tracker.add_past_sale(AuctionItem(id="2", artist="Artist A", title="Work 2", price=2000, region="mid-Atlantic"))
    tracker.add_past_sale(AuctionItem(id="3", artist="Artist B", title="Work 3", price=5000, region="mid-Atlantic"))

    analyzer = MarketAnalyzer(tracker)
    listing = AuctionItem(id="4", artist="Artist A", title="Work 4", estimated_price=1200, region="mid-Atlantic")

    expected_value = analyzer.calculate_expected_value(listing)
    assert expected_value == 1500.0  # Average of 1000 and 2000

def test_calculate_expected_value_no_past_sales():
    tracker = AuctionTracker()
    analyzer = MarketAnalyzer(tracker)
    listing = AuctionItem(id="1", artist="Artist C", title="Work 1", estimated_price=1200, region="mid-Atlantic")

    expected_value = analyzer.calculate_expected_value(listing)
    assert expected_value is None

def test_calculate_expected_value_school_of():
    tracker = AuctionTracker()
    tracker.add_past_sale(AuctionItem(id="1", artist="Famous Artist", title="Work 1", price=10000, region="mid-Atlantic"))
    tracker.add_past_sale(AuctionItem(id="2", artist="Famous Artist", title="Work 2", price=20000, region="mid-Atlantic"))

    analyzer = MarketAnalyzer(tracker)
    listing = AuctionItem(id="3", artist="School of Famous Artist", title="Work 3", estimated_price=1000, region="mid-Atlantic")

    # Let's say a "School of" piece is estimated at 10% of the famous artist's average
    expected_value = analyzer.calculate_expected_value(listing)
    assert expected_value == 1500.0 # 10% of 15000
