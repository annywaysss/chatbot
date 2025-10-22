import pathway as pw
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import io
import sys
import json
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)
MEMORY_FILE = "user_memory.json"

class ChatSchema(pw.Schema):
    user_id: int
    message: str
@pw.udf
def ask_gemini(query: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=query,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=1000
            )
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"
def save_user_detail(user_id, name=None, account_number=None):
    
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)
    else:
        memory = {}

    memory[str(user_id)] = {
        "name": name,
        "account_number": account_number
    }

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def get_user_detail(user_id):
    """Retrieve stored user info."""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)
        return memory.get(str(user_id), {})
    return {}


def get_pathway_console_output(user_id: int, user_message: str) -> str:
   
    table = pw.debug.table_from_rows(
        rows=[(user_id, user_message)],
        schema=ChatSchema
    )

    output_table = table.select(
        table.user_id,
        table.message,
        response=ask_gemini(table.message)
    )


    buffer = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = buffer

    try:
        pw.debug.compute_and_print(output_table)
    finally:
        sys.stdout = sys_stdout

    console_output = buffer.getvalue()
    return console_output


import re
from nlp_utils import extract_entities

def store_user_info(user_id, user_message):
   
    entities = extract_entities(user_message)
    name = None
    for label, entity in entities:
        if label == "PERSON":
            name = entity

    account_number = None
    match = re.search(r"\b\d{4,10}\b", user_message)
    if match:
        account_number = match.group()

    save_user_detail(user_id, name, account_number)
    return name, account_number