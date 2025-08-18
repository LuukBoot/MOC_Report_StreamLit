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

    def _extract_date(self) -> str:
        lines = self.text.strip().splitlines()
        date_line = lines[0].strip()
        return date_line.split(":")[1].strip()

    def _parse(self):
        self._parse_windows()
        self._parse_sections()

    def _parse_windows(self):
        lines = self.text.strip().splitlines()
        for i, line in enumerate(lines):
            if line.strip().startswith("Window dates:"):
                # same-line data
                after_colon = line.split(":", 1)[1].strip()
                if after_colon:
                    match = re.match(r"(FE|MW|BE)[\t ]+(\d{1,2}-\d{1,2}(?:\s+\w+)?)", after_colon)
                    if match:
                        self.windows.append(Windows(type=match.group(1), Dates=match.group(2)))

                for j in range(i + 1, min(i + 5, len(lines))):
                    l = lines[j].strip()
                    match = re.match(r"(FE|MW|BE)[\t ]+(\d{1,2}-\d{1,2}(?:\s+\w+)?)", l)
                    if match:
                        self.windows.append(Windows(type=match.group(1), Dates=match.group(2)))
                break

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
                        self.trades.append(RawTradeText(product=product, text=raw_text))

                elif "Average Price" in line:
                    match = re.search(r"\$([\d.]+)", line)
                    if match:
                        if not first_avg_price_found:
                            avg_price = float(match.group(1))
                            first_avg_price_found = True
                        else:
                            cum_avg_price = float(match.group(1))

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
                avg_price=avg_price,
                week_avg_price=cum_avg_price,
                cum_volume=cum_volume,
                total_volume=total_volume,
                week_volume=week_volume
            ))

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
