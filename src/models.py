from dataclasses import dataclass
from typing import Optional


@dataclass
class RawTradeText:
    product: str 
    text: str
    type: str  # "trade" or "last bid" or "last offer"


# update
@dataclass
class Trade:
    date: str
    product: str
    price: float
    volume_kt: float
    buyer: str
    seller: str
    window: str
    raw_text: str
    type: str # "trade" or "last bid" or "last offer"

    
    
@dataclass
class Offers_Bids:
    date: str
    product: str
    type: str  # "offer" or "bid"
    participant: str
    price: float
    window: str
    
@dataclass
class Windows:
    type: str
    Dates: str
    
    
@dataclass
class OverView:
    date: str
    product: str
    day_avg_price: Optional[float]
    week_avg_price: Optional[float]
    cum_volume: Optional[float]
    total_volume: Optional[float]
    week_volume: Optional[float]