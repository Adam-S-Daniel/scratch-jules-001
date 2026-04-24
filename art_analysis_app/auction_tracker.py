from dataclasses import dataclass
from typing import List, Optional

@dataclass
class AuctionItem:
    id: str
    artist: str
    title: str
    region: str
    price: Optional[float] = None
    estimated_price: Optional[float] = None
    medium: Optional[str] = None
    is_unidentified: bool = False

class AuctionTracker:
    def __init__(self):
        self.past_sales: List[AuctionItem] = []
        self.current_listings: List[AuctionItem] = []

    def add_past_sale(self, item: AuctionItem):
        self.past_sales.append(item)

    def add_current_listing(self, item: AuctionItem):
        self.current_listings.append(item)

    def get_mid_atlantic_past_sales(self) -> List[AuctionItem]:
        return [item for item in self.past_sales if item.region.lower() == "mid-atlantic"]

    def get_mid_atlantic_current_listings(self) -> List[AuctionItem]:
        return [item for item in self.current_listings if item.region.lower() == "mid-atlantic"]
