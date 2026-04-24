import pytest
from art_analysis_app.auction_tracker import AuctionItem, AuctionTracker
from art_analysis_app.market_analyzer import MarketAnalyzer
from art_analysis_app.opportunity_identifier import OpportunityIdentifier

def test_identify_opportunities():
    tracker = AuctionTracker()
    # Past sales for Artist A (average $2000)
    tracker.add_past_sale(AuctionItem(id="1", artist="Artist A", title="Work 1", price=1500, region="mid-Atlantic"))
    tracker.add_past_sale(AuctionItem(id="2", artist="Artist A", title="Work 2", price=2500, region="mid-Atlantic"))

    # Past sales for Famous Artist (average $50,000)
    tracker.add_past_sale(AuctionItem(id="3", artist="Famous Artist", title="Work 3", price=50000, region="mid-Atlantic"))

    # Current listings
    # Undervalued: Expected $2000, estimated $1000 (50% gap) -> Opportunity
    listing1 = AuctionItem(id="4", artist="Artist A", title="Work 4", estimated_price=1000, region="mid-Atlantic")
    tracker.add_current_listing(listing1)

    # Fairly valued: Expected $2000, estimated $1900 (5% gap) -> Not an opportunity
    listing2 = AuctionItem(id="5", artist="Artist A", title="Work 5", estimated_price=1900, region="mid-Atlantic")
    tracker.add_current_listing(listing2)

    # School of opportunity: Expected $5000 (10%), estimated $2000 (60% gap) -> Opportunity
    listing3 = AuctionItem(id="6", artist="School of Famous Artist", title="Work 6", estimated_price=2000, region="mid-Atlantic")
    tracker.add_current_listing(listing3)

    # No expected value -> Not an opportunity (at least based on price gap)
    listing4 = AuctionItem(id="7", artist="Unknown Artist", title="Work 7", estimated_price=500, region="mid-Atlantic")
    tracker.add_current_listing(listing4)

    analyzer = MarketAnalyzer(tracker)
    # Require at least 30% discount to be an opportunity
    identifier = OpportunityIdentifier(analyzer, min_discount_threshold=0.30)

    opportunities = identifier.find_opportunities(tracker.current_listings)

    assert len(opportunities) == 2

    opp_ids = [opp['item'].id for opp in opportunities]
    assert "4" in opp_ids
    assert "6" in opp_ids

    # Verify gap calculations
    opp_4 = next(opp for opp in opportunities if opp['item'].id == "4")
    assert opp_4['expected_value'] == 2000.0
    assert opp_4['discount_percentage'] == 0.50

    opp_6 = next(opp for opp in opportunities if opp['item'].id == "6")
    assert opp_6['expected_value'] == 5000.0
    assert opp_6['discount_percentage'] == 0.60
