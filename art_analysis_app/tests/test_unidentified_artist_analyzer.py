import pytest
from art_analysis_app.auction_tracker import AuctionItem, AuctionTracker
from art_analysis_app.unidentified_artist_analyzer import UnidentifiedArtistAnalyzer

def test_analyze_unidentified_artists():
    tracker = AuctionTracker()

    # Clearly identified artist
    item1 = AuctionItem(id="1", artist="Famous Artist", title="Work 1", region="mid-Atlantic", medium="oil on canvas")
    tracker.add_current_listing(item1)

    # Unidentified, but "School of"
    item2 = AuctionItem(id="2", artist="School of Famous Artist", title="Work 2", region="mid-Atlantic", is_unidentified=True, medium="oil on canvas")
    tracker.add_current_listing(item2)

    # Unidentified, high quality medium
    item3 = AuctionItem(id="3", artist="Unknown", title="Work 3", region="mid-Atlantic", is_unidentified=True, medium="oil on canvas")
    tracker.add_current_listing(item3)

    # Unidentified, low quality medium
    item4 = AuctionItem(id="4", artist="Unknown", title="Work 4", region="mid-Atlantic", is_unidentified=True, medium="pencil sketch")
    tracker.add_current_listing(item4)

    # "Circle of"
    item5 = AuctionItem(id="5", artist="Circle of Famous Artist", title="Work 5", region="mid-Atlantic", is_unidentified=True, medium="watercolor")
    tracker.add_current_listing(item5)

    analyzer = UnidentifiedArtistAnalyzer(tracker)

    promising_works = analyzer.find_promising_works()

    # Should find item2 ("School of"), item3 ("oil on canvas"), and item5 ("Circle of")
    assert len(promising_works) == 3

    ids = [work.id for work in promising_works]
    assert "2" in ids
    assert "3" in ids
    assert "5" in ids
    assert "1" not in ids
    assert "4" not in ids
