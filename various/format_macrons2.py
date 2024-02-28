import unicodedata

def process_polytonic_greek(text):
    processed_text = ''
    positions = []  # List to store positions and types of diacritics (macron or breve)
    
    for index, char in enumerate(text):
        decomposed_char = unicodedata.normalize('NFD', char)
        
        # Initialize variables to store the base character and its diacritics
        base_char = ''
        diacritics = ''
        
        # Iterate over each component in the decomposed character
        for component in decomposed_char:
            if component == '\u0304':  # Macron
                positions.append((index, '_'))
                continue
            elif component == '\u0306':  # Breve
                positions.append((index, '^'))
                continue
            elif unicodedata.category(component).startswith('M'):  # Diacritical mark
                diacritics += component
            else:
                base_char = component  # Base character
        
        # Reconstruct the character without the macron or breve
        reconstructed_char = base_char + diacritics
        # Re-normalize to recompose the character with its diacritics
        processed_text += unicodedata.normalize('NFC', reconstructed_char)
    
    return (processed_text, positions)

# Test the function with a sample polytonic Greek string
#sample_text = "Αἰαίᾱ Αἰγυπτῐ́ων"
#processed_text, positions = process_polytonic_greek(sample_text)
#print(processed_text)  # Processed text without _ or ^
#print(positions)  # List of tuples with position and type of diacritic

def append_symbols_to_text(positions, text):
    """
    Appends symbols ('_' or '^') to the specified positions in the text.
    
    Args:
        positions (list of tuples): A list where each tuple contains an index (int)
                                    and a symbol ('_' or '^').
        text (str): The text to which the symbols will be appended.
    
    Returns:
        str: The text with symbols appended at the specified positions.
    """
    # Sort the positions by index to handle them in order
    positions_sorted = sorted(positions, key=lambda x: x[0])
    
    # Offset to keep track of the number of characters we've inserted
    offset = 0

    for pos, symbol in positions_sorted:
        actual_pos = pos + offset + 1  # Adjust position by the offset and add 1
        # Insert symbol at the correct position
        text = text[:actual_pos] + symbol + text[actual_pos:]
        # Increase the offset by the length of the symbol
        offset += len(symbol)
    
    return text

# Test the function
sample_text = "Αἰαίᾱ Αἰγυπτῐ́ων"
positions = [(4, '_'), (12, '^')]  # Zero-based positions
result_text = append_symbols_to_text(positions, sample_text)
print(result_text)  # Expected output: "Αἰαία_ Αἰγυπτῐ́^ων"
