import re
from typing import List

def chunk_text(text: str, max_words: int = 200) -> List[str]:
    """
    Splits content into chunks (around `max_words` each).
    """
    words: List[str] = re.findall(r'\S+', text)
    chunks: List[str] = []
    
    for i in range(0, len(words), max_words):
        chunk_words = words[i:i + max_words]  # type: ignore
        chunks.append(" ".join(chunk_words))
        
    return chunks
