# scripts/prepare_data.py
"""
Generate a unified offline dataset for Transactly.
Combines optional open-source data (if present) with synthetic samples.
Outputs a clean CSV: data/processed/transactions.csv
"""
# scripts/prepare_data.py (top of file)
import sys, os
# add project root to sys.path so `import app...` works when running the script directly
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.core.category_taxonomy import get_categories
import os
import pandas as pd
import random
from faker import Faker

fake = Faker()
random.seed(42)

RAW_PATH = "data/raw"
OUTPUT_PATH = "data/processed/transactions.csv"

# Some example merchants per category (used to synthesize transactions)
MERCHANT_TEMPLATES = {
    "Food & Dining": ["Zomato", "Swiggy", "McDonalds", "Dominos", "KFC", "Starbucks"],
    "Shopping": ["Amazon", "Flipkart", "Myntra", "Ajio", "Meesho"],
    "Fuel": ["IndianOil", "HP Petrol", "BharatPetrol", "Shell"],
    "Travel & Transport": ["Uber", "Ola", "IRCTC", "AirIndia", "IndiGo"],
    "Utilities": ["Airtel Recharge", "BSNL Bill", "TNEB Payment", "Jio Fiber"],
    "Health & Fitness": ["Apollo Pharmacy", "1mg", "Cult Fit", "MedPlus"],
    "Entertainment": ["Netflix", "Hotstar", "Spotify", "BookMyShow"],
    "Bills & Subscriptions": ["YouTube Premium", "Google One", "Apple Music", "Canva Pro"],
    "Groceries": ["BigBasket", "Dunzo", "Reliance Fresh", "More Supermarket"],
    "Others": ["Unknown", "Misc Payment", "Transfer"]
}

def generate_synthetic_data(n_per_cat=300):
    """Generate synthetic transaction samples per category."""
    rows = []
    for category, merchants in MERCHANT_TEMPLATES.items():
        for _ in range(n_per_cat):
            merchant = random.choice(merchants)
            description = f"{merchant} payment #{random.randint(1000, 9999)}"
            amount = round(random.uniform(100, 5000), 2)
            txn_id = f"TXN{random.randint(100000,999999)}"
            rows.append([txn_id, description, amount, category])
    return pd.DataFrame(rows, columns=["transaction_id", "description", "amount", "category"])

def load_open_data():
    """Try to load any open dataset in data/raw folder."""
    for file in os.listdir(RAW_PATH):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(RAW_PATH, file))
            print(f"Loaded open dataset: {file} ({len(df)} rows)")
            return df
    return pd.DataFrame(columns=["transaction_id", "description", "amount", "category"])

def clean_and_merge(df_open, df_synth):
    """Clean text and merge open + synthetic data."""
    df = pd.concat([df_open, df_synth], ignore_index=True)
    df.drop_duplicates(subset=["description"], inplace=True)
    df["description"] = df["description"].astype(str).str.strip().str.lower()
    df["category"] = df["category"].astype(str).str.strip()
    return df.sample(frac=1, random_state=42).reset_index(drop=True)

def main():
    os.makedirs("data/processed", exist_ok=True)
    df_open = load_open_data()
    df_synth = generate_synthetic_data()
    df_final = clean_and_merge(df_open, df_synth)
    df_final.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Final dataset saved: {OUTPUT_PATH} ({len(df_final)} rows)")

if __name__ == "__main__":
    main()