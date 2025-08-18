from dataclasses import dataclass
from typing import Optional


@dataclass
class RawTradeText:
    product: str 
    text: str



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
    avg_price: Optional[float]
    week_avg_price: Optional[float]
    cum_volume: Optional[float]
    total_volume: Optional[float]
    week_volume: Optional[float]