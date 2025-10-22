import spacy
import re
from memory import update_memory
nlp = spacy.load("en_core_web_sm")

FINANCIAL_TERMS = {
    "loan", "interest", "bank", "credit", "investment",
    "mutual", "fund", "tax", "account", "insurance", "finance"
}

def extract_keywords(text: str):
    doc = nlp(text.lower())
    words = [token.text for token in doc if token.is_alpha]
    return [word for word in words if word in FINANCIAL_TERMS]

def extract_entities(text: str):
   
    doc = nlp(text)
    return [(ent.label_, ent.text) for ent in doc.ents]

def extract_user_details(text: str, user_id: int):
    details = {}

    name_patterns = [
        r"my name is (\w+)",
        r"i am (\w+)",
        r"this is (\w+)"
    ]
    for pattern in name_patterns:
        match = re.search(pattern, text, re.I)
        if match:
            details["name"] = match.group(1)
            break

    account_num_match = re.search(r"account number\s*(?:is|=)?\s*(\d+)", text, re.I)
    if account_num_match:
        details["account_number"] = account_num_match.group(1)
    pin_match = re.search(r"(pin|password)\s*(?:is|=)?\s*(\d+)", text, re.I)
    if pin_match:
        details["pin"] = pin_match.group(2)
    account_type_match = re.search(r"(savings|checking|current) account", text, re.I)
    if account_type_match:
        details["account_type"] = account_type_match.group(1)
    investment_match = re.search(r"(stocks|mutual funds|crypto|bonds|real estate)", text, re.I)
    if investment_match:
        details["investment_interest"] = investment_match.group(1)

    return details
