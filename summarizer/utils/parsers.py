from typing import Tuple


def extract_text_and_pages(file_bytes: bytes, mimetype: str) -> Tuple[str, int]:
    """
    Instead of parsing locally, this just prepares the file
    to be sent to the external ML model.
    
    For now, returns empty text and 0 pages.
    The ML model is expected to handle parsing + summarization.
    """
    return "", 0
