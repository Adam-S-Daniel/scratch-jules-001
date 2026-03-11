from typing import List
from art_analysis_app.auction_tracker import AuctionTracker, AuctionItem

class UnidentifiedArtistAnalyzer:
    def __init__(self, tracker: AuctionTracker):
        self.tracker = tracker
        self.clue_keywords = ["school of", "circle of", "follower of", "style of", "manner of", "after"]
        self.high_quality_mediums = ["oil on canvas", "oil on board", "acrylic on canvas", "bronze", "marble"]

    def find_promising_works(self) -> List[AuctionItem]:
        promising_works = []

        for listing in self.tracker.current_listings:
            if not listing.is_unidentified:
                continue

            is_promising = False

            # Check for association clues in the artist name or description (here using artist field as a proxy for attribution)
            artist_lower = listing.artist.lower()
            if any(clue in artist_lower for clue in self.clue_keywords):
                is_promising = True

            # Check for high quality mediums
            if listing.medium and listing.medium.lower() in self.high_quality_mediums:
                is_promising = True

            if is_promising:
                promising_works.append(listing)

        return promising_works
