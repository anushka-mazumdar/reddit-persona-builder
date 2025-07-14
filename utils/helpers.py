import os
import re
import json

def clean_text(text: str) -> str:
    """
    Basic text cleaner: removes extra whitespace, markdown, and escapes.
    """
    if not isinstance(text, str):
        return ""
    text = re.sub(r'\s+', ' ', text)  # normalize whitespace
    text = text.replace('\\n', ' ').replace('\n', ' ').strip()
    return text

def save_json(data, path: str):
    """
    Saves a Python object as a formatted JSON file.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(path: str):
    """
    Loads and returns JSON data from a file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def cite_text(source_text: str, max_len: int = 100) -> str:
    """
    Returns a short citation string from a longer text.
    """
    cleaned = clean_text(source_text)
    return f"“{cleaned[:max_len]}...”" if len(cleaned) > max_len else f"“{cleaned}”"

def safe_filename(name: str) -> str:
    """
    Returns a filesystem-safe version of a filename or username.
    """
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

