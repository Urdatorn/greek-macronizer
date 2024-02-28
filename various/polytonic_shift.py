import unicodedata

def lower_polytonic(text):
    """
    Converts a polytonic Greek string to lowercase.
    
    This function takes into account the diacritical marks used in polytonic Greek and ensures they are preserved when transforming the characters to lowercase.
    
    Args:
        text (str): The polytonic Greek text to be converted to lowercase.
    
    Returns:
        str: The input text converted to lowercase.
    
    Example:
        sample_text = "Αἰακίδας"
        result = to_lower_polytonic_greek(sample_text)
        print(result)  # Output: αἰακίδας
    """
    return unicodedata.normalize('NFC', text.lower())

def upper_polytonic(text):
    """
    Converts a polytonic Greek string to uppercase.
    
    This function takes into account the diacritical marks used in polytonic Greek and ensures they are preserved and properly placed when transforming the characters to uppercase.
    
    Args:
        text (str): The polytonic Greek text to be converted to uppercase.
    
    Returns:
        str: The input text converted to uppercase.
    
    Example:
        sample_text = "αἰακίδας"
        result = to_upper_polytonic_greek(sample_text)
        print(result)  # Output: ΑΙΑΚΙΔΑΣ
    """
    # Normalize the text to NFD (Normalization Form Decomposed) form to separate the diacritics from the base characters
    text_nfd = unicodedata.normalize('NFD', text)

    # Convert to uppercase and then normalize to NFC form to compose the characters and diacritics
    return unicodedata.normalize('NFC', text_nfd.upper())
