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
    "Financial Services": [
        # 1. Bank Transfers
        "IMPS Transfer", "NEFT Transfer", "RTGS Transfer", "Bank A/C Transfer",
        
        # 2. UPI
        "PhonePe UPI", "GooglePay UPI", "Paytm UPI", "BHIM UPI", "AmazonPay UPI",
    
        # 3. ATM
        "ATM Withdrawal", "SBI ATM", "HDFC ATM", "ICICI ATM", "ATM Cash Removal",
    
        # 4. Card Payments
        "Debit Card Payment", "Credit Card POS", "Card Swipe",
    
        # 5. Loan / EMI
        "HDFC Loan EMI", "ICICI EMI Payment", "Bajaj Finance EMI", 
    
        # 6. Bank Charges
        "Bank Service Charge", "ATM Fee", "SMS Charge", "Reversal Charge",
    
        # 7. Salary / Income
        "Salary Credit", "Incentive Payment", "Company Reimbursement",
    
        # 8. Credit Card Bills
        "HDFC Credit Card", "ICICI Credit Card", "SBI Card Payment",
    ],
    "Food & Dining": [
        "Zomato", "Swiggy", "McDonalds", "Dominos", "KFC", "Starbucks",
        "Kritunga", "Chai Point", "Barbeque Nation", "Faasos", "Behrouz Biryani",
        "Wow Momo", "CCD Cafe", "Burger King", "Pizza Hut", "Subway",
        "Chai Sutta Bar", "Haldirams", "Bikanervala", "Paradise Biryani",
        "Brewberrys Cafe", "Thai Pavilion", "Cafe Coffee Day", "Chayos",
    ],
    "Shopping": [
        "Amazon", "Flipkart", "Myntra", "Ajio", "Meesho",
        "D Mart", "Croma", "Reliance Trends", "Nykaa", "Tanishq",
        "FirstCry", "Decathlon", "Lifestyle", "Shoppers Stop", "Tata Cliq",
        "Pantaloons", "Westside", "Zara India", "H&M India", "V Mart",
    ],
    "Fuel": [
        "IndianOil", "HP Petrol", "BharatPetrol", "Shell",
        "Reliance Petrol Pump", "Essar Petrol", "Nayara Energy",
        "IOC Fuel Station", "BPCL Fuel Outlet", "HPCL Pump",
    ],
    "Travel & Transport": [
        "Uber", "Ola", "IRCTC", "AirIndia", "IndiGo",
        "Rapido", "RedBus", "AbhiBus", "MakeMyTrip", "Goibibo",
        "Vistara Airlines", "Yatra Travels", "BlaBlaCar", "Orix Cabs",
        "KSRTC Bus", "TNSTC Bus Service",
    ],
    "Utilities": [
        "Airtel Recharge", "BSNL Bill", "TNEB Payment", "Jio Fiber",
        "ACT Fibernet", "Vodafone Idea Recharge", "Hathway Broadband",
        "Tata Play DTH", "Airtel Digital TV", "Municipal Water Tax",
        "Adani Electricity", "Torrent Power", "BESCOM Electricity",
    ],
    "Health & Fitness": [
        "Apollo Pharmacy", "1mg", "Cult Fit", "MedPlus",
        "PharmEasy", "Healthspring", "Dr Lal PathLabs",
        "Fortis Hospital", "Max Healthcare", "Columbia Asia",
        "Viva Fitness Gym", "Gold’s Gym India", "Talwalkars Gym",
    ],
    "Entertainment": [
        "Netflix", "Hotstar", "Spotify", "BookMyShow",
        "PVR Cinemas", "INOX Movies", "Zee5 Subscription",
        "Amazon Prime Video", "ALT Balaji", "Gaana Plus",
        "PlayStation Store", "Xbox Live", "IRL Events India",
    ],
    "Bills & Subscriptions": [
        "YouTube Premium", "Google One", "Apple Music", "Canva Pro",
        "Notion Subscription", "Adobe Creative Cloud", "Microsoft 365",
        "Figma Pro", "Coursera Plus", "Spotify Premium",
        "ZEE5 Premium", "Disney Plus Hotstar", "Prime Membership",
    ],
    "Groceries": [
        "BigBasket", "Dunzo", "Reliance Fresh", "More Supermarket",
        "Blinkit", "Nature's Basket", "Spencer’s Retail",
        "Heritage Fresh", "JioMart Grocery", "Easyday Club",
        "DMart Ready", "Nilgiris Supermarket",
    ],
    "Others": [
        "Unknown", "Misc Payment", "Transfer",
        "UrbanClap", "Urban Company", "HouseJoy",
        "NoBroker Services", "Local Technician", "Freelancer Payment",
        "Donation Payment", "Society Maintenance", "Parking Charges",
    ]
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