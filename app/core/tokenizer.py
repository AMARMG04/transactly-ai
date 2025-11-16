import re

def smart_tokenize(text: str):
    """
    Splits IRCTCbookedTXN → IRCTC booked TXN
    Splits CamelCase, digits, symbols.
    """
    # Split camelcase
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

    # Replace separators
    text = text.replace("_", " ").replace("-", " ")

    # Extract tokens
    tokens = re.findall(r"[A-Za-z]+|\d+|[^\w\s]", text)

    return tokens