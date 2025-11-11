# app/core/rules.py
"""
Step 6 – Rules & Precision Boosters
Merchant-level or pattern-based rules to override or reinforce model predictions.
"""

import re

# ⚙️ Hardcoded rules: merchant patterns → canonical category
# Keep these simple and readable (can later load from rules.yaml)
RULES = {
    r"\b(irctc|airindia|indigo|goair|spicejet|uber|ola)\b": "Travel & Transport",
    r"\b(indianoil|hpcl|hindustan petroleum|bharatpetrol|shell)\b": "Fuel",
    r"\b(zomato|swiggy|dominos|kfc|mcdonalds|starbucks)\b": "Food & Dining",
    r"\b(amazon|flipkart|myntra|ajio|meesho|reliance trends)\b": "Shopping",
    r"\b(apollo pharmacy|1mg|medplus|pharmeasy|cult fit|gym)\b": "Health & Fitness",
    r"\b(netflix|hotstar|spotify|bookmyshow|pvr|youtube premium|apple tv)\b": "Entertainment",
    r"\b(tneb|bsnl|airtel|jio fiber|vi recharge|electricity bill|gas bill)\b": "Utilities",
    r"\b(bigbasket|reliance fresh|dunzo|more supermarket)\b": "Groceries",
    r"\b(google one|canva pro|dropbox|office 365|prime membership)\b": "Bills & Subscriptions",
}


def apply_rules(text: str):
    """
    Check description against predefined rules.
    Returns (category, matched_pattern) if hit, else (None, None).
    """
    text = text.lower().strip()
    for pattern, category in RULES.items():
        if re.search(pattern, text):
            return category, pattern
    return None, None


# 🧪 Test demo
if __name__ == "__main__":
    samples = [
        "IRCTC train booking #7845",
        "Payment to IndianOil Chennai",
        "Zomato order #92384",
        "Amazon purchase 8293",
        "Netflix subscription 499",
        "Airtel Bill Payment",
        "Apollo Pharmacy invoice",
        "BigBasket Groceries Order",
        "Spotify premium charge",
        "Transfer to unknown merchant"
    ]

    for s in samples:
        cat, pat = apply_rules(s)
        print(f"{s:35} → {cat or 'No rule match'}  ({pat or '-'})")