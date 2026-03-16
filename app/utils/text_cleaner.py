import re

def clean_text(text: str) -> str:
    """
    Cleans extracted text by removing unnecessary characters and normalizing whitespace.
    """
    if not text:
        return ""
    # Remove null bytes
    text = text.replace('\x00', '')
    # Replace multiple newlines or spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing whitespace
    return text.strip()
