from .models import Trade, Offers_Bids, Windows, OverView, RawTradeText
import re
from typing import List, Optional

class ParsedReport:
    def __init__(self, text: str):
        self.text = text
        self.date = self._extract_date()
        self.windows: List[Windows] = []
        self.trades: List[RawTradeText] = []
        self.offers_bids: List[Offers_Bids] = []
        self.overviews: List[OverView] = []
        self._parse()
        self.set_type_for_trades()

    def _extract_date(self) -> str:
        lines = self.text.strip().splitlines()
        date_line = lines[0].strip()
        return date_line.split(":")[1].strip()

    def _parse(self):
        self._parse_windows()
        self._parse_sections()

    def _parse_windows(self):
        lines = self.text.strip().splitlines()
        
        # Look for window data in all lines, not just after "Window dates:"
        for line in lines:
            line = line.strip()
            if line:
                # Match window type followed by whitespace and date range
                match = re.match(r"(FE|MW|BE)\s+(\d{1,2}-\d{1,2}(?:\s+\w+)?)", line)
                if match:
                    self.windows.append(Windows(type=match.group(1), Dates=match.group(2)))

    def _parse_sections(self):
        product_sections = re.split(r"=+\n", self.text)[1:]

        for section in product_sections:
            lines = [line.strip() for line in section.strip().splitlines() if line.strip()]
            if not lines:
                continue

            product = lines[0].replace(":", "").strip()
            current_offers = []
            current_bids = []

            # overview values
            avg_price = None
            total_volume = None
            week_volume = None
            cum_volume = None
            cum_avg_price = None
            first_avg_price_found = False
            
            print("Processing product:", product)
            
            

            for i, line in enumerate(lines[1:]):
                if line.startswith("Offers"):
                    current_offers = re.split(r'[:/]', line.split(":", 1)[1].strip())
                    for p in current_offers:
                        self.offers_bids.append(Offers_Bids(
                            date=self.date, product=product, type="offer",
                            participant=p.strip(), price=0.0, window="N/A"))

                elif line.startswith("Bids"):
                    current_bids = re.split(r'[:/]', line.split(":", 1)[1].strip())
                    for p in current_bids:
                        self.offers_bids.append(Offers_Bids(
                            date=self.date, product=product, type="bid",
                            participant=p.strip(), price=0.0, window="N/A"))

                elif line.startswith("Trades"):
                    trade_lines = []
                    for trade_line in lines[i+2:]:
                        if not trade_line.strip() or "Average Price" in trade_line:
                            break
                        trade_lines.append(trade_line)
                    if trade_lines:
                        raw_text = "\n".join(trade_lines)
                        self.trades.append(RawTradeText(product=product, text=raw_text, type="Trades"))

                elif "Average Price" in line:
                    # Try to match both "$-1.38" and "$ -1.38" and also handle possible tabs/spaces
                    match = re.search(r"\$\s*(-?\d+(?:\.\d+)?)", line)
                    if match:
                        if first_avg_price_found:
                            cum_avg_price = float(match.group(1))
                        else:
                            avg_price = float(match.group(1))
                            first_avg_price_found = True

                elif "Total Volume" in line and "this week" not in line:
                    match = re.search(r":\s*([\d.]+)", line)
                    if match:
                        total_volume = float(match.group(1))

                elif "Total volume this week" in line:
                    match = re.search(r":\s*([\d.]+)", line)
                    if match:
                        week_volume = float(match.group(1))

                elif "All volume up till now" in line:
                    match = re.search(r":\s*([\d.]+)", line)
                    if match:
                        cum_volume = float(match.group(1))

            self.overviews.append(OverView(
                date=self.date,
                product=product,
                day_avg_price=avg_price,
                week_avg_price=cum_avg_price,
                cum_volume=cum_volume,
                total_volume=total_volume,
                week_volume=week_volume
            ))

    def set_type_for_trades(self):
        new_trades = []
        
        for trade in self.trades:
            text = trade.text.strip()
            
            # Check if the text contains "last bid" or "last offer"
            has_last_bid = "last bid" in text.lower()
            has_last_offer = "last offer" in text.lower()
            
            if has_last_bid or has_last_offer:
                # Split the text by lines to handle multiple last bids/offers
                lines = text.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                        
                    if line.lower().startswith("last bid"):
                        # Extract everything after "last bid"
                        bid_text = line[8:].strip()  # Remove "last bid" prefix
                        new_trades.append(RawTradeText(
                            product=trade.product,
                            text=bid_text,
                            type="last bid"
                        ))
                    elif line.lower().startswith("last offer"):
                        # Extract everything after "last offer"
                        offer_text = line[10:].strip()  # Remove "last offer" prefix
                        new_trades.append(RawTradeText(
                            product=trade.product,
                            text=offer_text,
                            type="last offer"
                        ))
                    else:
                        # If it's not a last bid/offer line, treat as regular trade
                        new_trades.append(RawTradeText(
                            product=trade.product,
                            text=line,
                            type="trade"
                        ))
            else:
                # No last bid or last offer, just regular trades
                trade.type = "trade"
                new_trades.append(trade)
        
        # Replace the old trades list with the new one
        self.trades = new_trades

    def get_window_data(self) -> List[Windows]:
        return self.windows

    def get_offers_bids(self) -> List[Offers_Bids]:
        return self.offers_bids

    def get_trades(self) -> List[RawTradeText]:
        return self.trades

    def get_overviews(self) -> List[OverView]:
        return self.overviews

    def count_trades(self) -> int:
        return len(self.trades)
