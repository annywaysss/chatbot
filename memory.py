import json
import os

MEMORY_FILE = "user_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def update_memory(user_id: int, key: str, value: str):
   
    memory = load_memory()
    user_key = str(user_id)
    if user_key not in memory:
        memory[user_key] = {}
    memory[user_key][key] = value
    save_memory(memory)

def get_user_memory(user_id: int):
    memory = load_memory()
    return memory.get(str(user_id), {})
