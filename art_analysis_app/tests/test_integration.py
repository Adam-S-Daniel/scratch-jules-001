import pytest
from art_analysis_app.auction_tracker import AuctionTracker, AuctionItem
from art_analysis_app.market_analyzer import MarketAnalyzer
from art_analysis_app.opportunity_identifier import OpportunityIdentifier
from art_analysis_app.unidentified_artist_analyzer import UnidentifiedArtistAnalyzer

def test_full_pipeline_integration():
    # 1. Setup Tracker
    tracker = AuctionTracker()

    # 2. Add past sales data (Mid-Atlantic market context)
    past_sales_data = [
        AuctionItem(id="ps1", artist="Artist Alpha", title="Sunset", price=10000, region="mid-Atlantic"),
        AuctionItem(id="ps2", artist="Artist Alpha", title="Sunrise", price=15000, region="mid-Atlantic"),
        AuctionItem(id="ps3", artist="Artist Beta", title="Abstract I", price=5000, region="mid-Atlantic"),
        AuctionItem(id="ps4", artist="Artist Beta", title="Abstract II", price=5000, region="mid-Atlantic"),
        AuctionItem(id="ps5", artist="Master Painter", title="Masterpiece", price=100000, region="mid-Atlantic"),
        AuctionItem(id="ps6", artist="Master Painter", title="Another Masterpiece", price=150000, region="mid-Atlantic"),
    ]
    for item in past_sales_data:
        tracker.add_past_sale(item)

    # 3. Add current listings (Mid-Atlantic upcoming auctions)
    current_listings_data = [
        # Undervalued Alpha (Expected: 12500, Est: 5000 -> 60% discount) -> Opportunity
        AuctionItem(id="cl1", artist="Artist Alpha", title="Noon", estimated_price=5000, region="mid-Atlantic"),

        # Fairly valued Beta (Expected: 5000, Est: 4500 -> 10% discount) -> Not Opportunity
        AuctionItem(id="cl2", artist="Artist Beta", title="Abstract III", estimated_price=4500, region="mid-Atlantic"),

        # School of Master Painter (Expected: 10% of 125000 = 12500, Est: 3000 -> 76% discount) -> Opportunity AND Unidentified/Promising
        AuctionItem(id="cl3", artist="School of Master Painter", title="Study", estimated_price=3000, region="mid-Atlantic", is_unidentified=True, medium="oil on canvas"),

        # Unidentified but promising (oil on canvas)
        AuctionItem(id="cl4", artist="Unknown", title="Portrait", estimated_price=500, region="mid-Atlantic", is_unidentified=True, medium="oil on canvas"),

        # Unidentified, not promising (pencil)
        AuctionItem(id="cl5", artist="Unknown", title="Sketch", estimated_price=100, region="mid-Atlantic", is_unidentified=True, medium="pencil sketch"),
    ]
    for item in current_listings_data:
        tracker.add_current_listing(item)

    # 4. Filter for mid-Atlantic (mostly to ensure methods work as part of the flow)
    mid_atlantic_sales = tracker.get_mid_atlantic_past_sales()
    mid_atlantic_listings = tracker.get_mid_atlantic_current_listings()

    assert len(mid_atlantic_sales) == 6
    assert len(mid_atlantic_listings) == 5

    # 5. Analyze Market & Identify Opportunities
    analyzer = MarketAnalyzer(tracker)
    identifier = OpportunityIdentifier(analyzer, min_discount_threshold=0.30)
    opportunities = identifier.find_opportunities(mid_atlantic_listings)

    # We expect cl1 and cl3 to be opportunities based on expected value
    assert len(opportunities) == 2
    opp_ids = [opp['item'].id for opp in opportunities]
    assert "cl1" in opp_ids
    assert "cl3" in opp_ids

    # 6. Analyze Unidentified Artists for Promising Works
    unidentified_analyzer = UnidentifiedArtistAnalyzer(tracker)
    # Using the same list of mid-Atlantic current listings might require updating the UnidentifiedArtistAnalyzer to take listings directly, or ensuring the tracker state is used.
    # The current implementation of UnidentifiedArtistAnalyzer uses `self.tracker.current_listings`. Let's use that.
    promising_works = unidentified_analyzer.find_promising_works()

    # We expect cl3 ("School of", "oil on canvas") and cl4 ("oil on canvas") to be promising
    assert len(promising_works) == 2
    promising_ids = [work.id for work in promising_works]
    assert "cl3" in promising_ids
    assert "cl4" in promising_ids

    # Ensure cl5 is not there
    assert "cl5" not in promising_ids
