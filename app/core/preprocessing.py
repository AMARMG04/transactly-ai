# app/core/preprocessing.py
"""
Text normalization and merchant canonicalization for Transactly.
Ensures messy transaction strings like 'AMZN PMT #9283' → 'amazon'.
"""

import re
import unidecode
from rapidfuzz import process, fuzz

# Known abbreviations or common short forms
MERCHANT_ALIASES = {
    "amzn": "amazon",
    "fpt": "flipkart",
    "swg": "swiggy",
    "zmt": "zomato",
    "irctc": "irctc",
    "bpcl": "bharatpetrol",
    "ioc": "indianoil",
    "io": "indianoil",
    "bb": "bigbasket",
    "appl": "apple",
    "yt": "youtube",
    "bms": "bookmyshow",
    "pvr": "pvr cinemas",
    "mtx": "myntra",
    "rfr": "reliance fresh",
    "hdfc": "hdfc bank",
}

# Canonical merchant names (from your dataset)
CANONICAL_MERCHANTS = [
    "amazon", "flipkart", "myntra", "ajio", "meesho",
    "swiggy", "zomato", "dominos", "starbucks",
    "irctc", "uber", "ola", "indianoil", "hp petrol", "bharatpetrol",
    "airindia", "indigo", "tneb", "airtel", "bsnl", "jio fiber",
    "apollo pharmacy", "1mg", "cult fit", "medplus",
    "netflix", "hotstar", "spotify", "bookmyshow",
    "youtube premium", "google one", "apple music", "canva pro",
    "bigbasket", "dunzo", "reliance fresh", "more supermarket"
]


def clean_text(text: str) -> str:
    """Apply regex + unicode normalization to transaction text."""
    if not isinstance(text, str):
        return ""
    text = unidecode.unidecode(text)  # remove accents
    text = re.sub(r"[^A-Za-z0-9\s]", " ", text)  # remove symbols
    text = re.sub(r"\s+", " ", text)  # normalize spaces
    return text.strip().lower()


def canonicalize_merchant(text: str) -> str:
    """Normalize and map to canonical merchant name."""
    text = clean_text(text)

    # Try direct alias match
    for alias, canonical in MERCHANT_ALIASES.items():
        if re.search(rf"\b{alias}\b", text):
            return canonical

    # Fuzzy match against canonical list
    match, score, _ = process.extractOne(text, CANONICAL_MERCHANTS, scorer=fuzz.token_sort_ratio)
    if score >= 80:
        return match

    # Fallback: first token as guess (e.g., "swiggy order" -> "swiggy")
    parts = text.split()
    return parts[0] if parts else text


def normalize_transaction(description: str) -> str:
    """Full normalization pipeline."""
    clean_desc = clean_text(description)
    merchant = canonicalize_merchant(clean_desc)
    return merchant


# Demo run
if __name__ == "__main__":
    samples = [
        "AMZN PMT #9283",
        "Swg order ID 4389",
        "ZMT txn 829",
        "IRCTC train 9823",
        "Appl music charge",
        "BPCL Chennai",
        "YT premium 9384",
        "Flipkrt Order 123",
    ]
    for s in samples:
        print(f"{s} → {normalize_transaction(s)}")