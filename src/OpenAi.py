import os
from typing import List
from openai import OpenAI
import json
from .models import Trade, Offers_Bids, Windows, OverView, RawTradeText
import streamlit as st


openai_key = st.secrets["OPENAI_API_KEY"]



client = OpenAI(
    # This is the default and can be omitted
    api_key=openai_key,
)

def extract_trades_from_rawtext(raw_trade: RawTradeText, date: str) -> List[Trade]:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI that transforms raw trade text into structured JSON objects.\n"
                    "Your output must be strictly valid JSON — no markdown, no explanations.\n"
                    "Every trade in the input text must be one JSON object in an array.\n"
                    "You must detect trade boundaries yourself, even if trades are not separated by new lines.\n"
                    "Schema for each trade:\n"
                    "{\n"
                    '  "date": "string or null",\n'
                    '  "product": "string",\n'
                    '  "price": float or null, // always extract numeric value, may be negative, may be prefixed by $ or -\n'
                    '  "volume_kt": float or null,\n'
                    '  "buyer": "string or null // always the second company mentioned in a trade, never FE, MW, BE"\n'
                    '  "seller": "string or null // always the first company mentioned in a trade, never FE, MW, BE"\n'
                    '  "window": "string or null", // must be one of: "FE", "MW", "BE"\n'
                    '  "raw_text": "string"\n'
                    "}\n\n"
                    "Rules:\n"
                    "1. Always use the provided 'date' and 'product' values for every trade.\n"
                    "2. Extract 'window' exactly as 'FE', 'MW', or 'BE' from the trade line, or null if missing.\n"
                    "3. Include the exact original text for that trade in 'raw_text'.\n"
                    "4. Use null for any field where information is not present.\n"
                    "5. The number of JSON objects must equal the number of detected trades in the text.\n"
                    "6. Do not include any text outside the JSON output.\n"
                    "7. If type is equal to is trade than there are always two companies involved the first company is the seller and the second companay is the buyer\n"
                    "8. If type is equal to: last bid it ALWAYS includes an buyer and NO seller make seller equal to null \n"
                    "9. If type is equal to: last offer it ALWAYS includes an seller and NO buyer make buyer equal to null \n"
                )
            },
            {
                "role": "user",
                "content": (
                    f"Date: {date}\n"
                    f"Product: {raw_trade.product}\n"
                    f"Raw text:\n{raw_trade.text}\n"
                    f"Type: {raw_trade.type}\n"
                )
            }
        ],

    )

    json_result = json.loads(response.choices[0].message.content)
    trades = []
    for trade_dict in json_result:
        trades.append(Trade(
            date=trade_dict.get("date"),
            product=trade_dict.get("product"),
            price=trade_dict.get("price"),
            volume_kt=trade_dict.get("volume_kt"),
            buyer=trade_dict.get("buyer"),
            seller=trade_dict.get("seller"),
            window=trade_dict.get("window"),
            raw_text=trade_dict.get("raw_text"),
            type=raw_trade.type  # Use the type from the raw trade
        ))
    json_result = trades
    return json_result
