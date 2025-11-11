# app/core/category_taxonomy.py
"""
Defines the canonical spending categories used in Transactly.
All model training, rules, and predictions should refer to these constants.
"""

from typing import List, Dict

# ✅ Canonical categories
CATEGORIES: List[str] = [
    "Food & Dining",
    "Shopping",
    "Fuel",
    "Travel & Transport",
    "Utilities",
    "Health & Fitness",
    "Entertainment",
    "Bills & Subscriptions",
    "Groceries",
    "Others"
]

# ✅ Optional aliases / synonyms to normalize labels (for retraining or LLM bootstrap)
CATEGORY_ALIASES: Dict[str, List[str]] = {
    "Food & Dining": ["food", "restaurants", "dining", "eating out"],
    "Shopping": ["ecommerce", "online shopping", "retail"],
    "Fuel": ["petrol", "diesel", "gas station"],
    "Travel & Transport": ["transportation", "cab", "uber", "ola", "bus", "train", "flight"],
    "Utilities": ["electricity", "water", "gas", "internet", "mobile recharge"],
    "Health & Fitness": ["medical", "pharmacy", "hospital", "doctor", "gym"],
    "Entertainment": ["movies", "netflix", "music", "games", "ott"],
    "Bills & Subscriptions": ["subscription", "bill", "monthly plan"],
    "Groceries": ["supermarket", "vegetables", "daily needs", "mart"],
    "Others": ["misc", "general", "unknown"]
}

def get_categories() -> List[str]:
    """Return the canonical list of categories."""
    return CATEGORIES

def normalize_category(label: str) -> str:
    """Normalize a free-text label to a canonical category."""
    label = label.strip().lower()
    for canonical, aliases in CATEGORY_ALIASES.items():
        if label == canonical.lower() or label in aliases:
            return canonical
    return "Others"