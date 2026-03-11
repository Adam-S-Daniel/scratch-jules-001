import pytest
from art_analysis_app.auction_tracker import AuctionTracker, AuctionItem

def test_add_past_sale():
    tracker = AuctionTracker()
    item = AuctionItem(id="1", artist="Artist A", title="Work A", price=1000, region="mid-Atlantic")
    tracker.add_past_sale(item)
    assert len(tracker.past_sales) == 1
    assert tracker.past_sales[0].id == "1"

def test_add_current_listing():
    tracker = AuctionTracker()
    item = AuctionItem(id="2", artist="Artist B", title="Work B", estimated_price=1500, region="mid-Atlantic")
    tracker.add_current_listing(item)
    assert len(tracker.current_listings) == 1
    assert tracker.current_listings[0].id == "2"

def test_filter_mid_atlantic_sales():
    tracker = AuctionTracker()
    tracker.add_past_sale(AuctionItem(id="1", artist="Artist A", title="Work A", price=1000, region="mid-Atlantic"))
    tracker.add_past_sale(AuctionItem(id="2", artist="Artist B", title="Work B", price=2000, region="west-coast"))

    mid_atlantic_sales = tracker.get_mid_atlantic_past_sales()
    assert len(mid_atlantic_sales) == 1
    assert mid_atlantic_sales[0].id == "1"

def test_filter_mid_atlantic_listings():
    tracker = AuctionTracker()
    tracker.add_current_listing(AuctionItem(id="3", artist="Artist C", title="Work C", estimated_price=1000, region="mid-Atlantic"))
    tracker.add_current_listing(AuctionItem(id="4", artist="Artist D", title="Work D", estimated_price=2000, region="europe"))

    mid_atlantic_listings = tracker.get_mid_atlantic_current_listings()
    assert len(mid_atlantic_listings) == 1
    assert mid_atlantic_listings[0].id == "3"
