import pdfplumber
from typing import IO

def extract_text(file_obj: IO) -> str:
    """
    Extracts text from a given PDF file object using pdfplumber.
    """
    full_text = ""
    with pdfplumber.open(file_obj) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += str(text) + "\n"  # type: ignore
    return full_text
