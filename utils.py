import re
import string
import unicodedata

class Colors:
    GREEN = '\033[1;32m'  # Green
    RED = '\033[1;31m'    # Red
    ENDC = '\033[0m'      # Reset to default color
    YELLOW = '\033[1;33m' # Yellow
    BLUE = '\033[1;34m'   # Blue
    MAGENTA = '\033[1;35m'# Magenta
    CYAN = '\033[1;36m'   # Cyan
    WHITE = '\033[1;37m'  # White
    BOLD = '\033[1m'      # Bold
    UNDERLINE = '\033[4m' # Underline

# Mapping of Beta Code letters to their sorting order. no 'J' or 'V'
BETA_CODE_ORDER = {
    'A': 1, 'B': 2, 'G': 3, 'D': 4, 'E': 5, 'Z': 6, 'H': 7, 'Q': 8,
    'I': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'C': 14, 'O': 15,
    'P': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'F': 21, 'X': 22,
    'Y': 23, 'W': 24
}

def beta_code_sort_key(word):
    """
    Returns a list of numbers representing the sorting order of each character in a word,
    based on the Beta Code order. Ignores characters not in BETA_CODE_ORDER.
    """
    # Filter to include only characters present in BETA_CODE_ORDER, converting to uppercase to match the dictionary keys
    filtered_chars = [char.upper() for char in word if char.upper() in BETA_CODE_ORDER]
    return [BETA_CODE_ORDER.get(char, 0) for char in filtered_chars]

# Unicode Constants
GREEK_ANO_TELEIA = '\u0387'
GREEK_QUESTION_MARK = '\u037E'
DAGGER = '\u2020'
EM_DASH = '\u2014'

# Unicode ranges for Greek characters
MONOTONIC_CHARS = set(range(0x391, 0x3A9 + 1)).union(range(0x3B1, 0x3C9 + 1)) - {GREEK_ANO_TELEIA, GREEK_QUESTION_MARK}
POLYPHONIC_CHARS = set(range(0x1F00, 0x1FFF + 1))

# Merge both sets for a unified set of Greek characters
GREEK_CHARS = MONOTONIC_CHARS.union(POLYPHONIC_CHARS)

# Function to check if the string contains any Greek letters
def contains_greek(text):
    """
    Check if the provided text contains any Greek characters.
    
    Args:
        text (str): The text string to be checked for Greek characters.
    
    Returns:
        bool: True if the text contains any Greek characters, False otherwise.
    """
    return any(char in GREEK_CHARS for char in map(ord, text))

# Function to remove surrounding punctuation and dagger from Greek characters
def remove_surrounding_punctuation(token_or_lemma):
    """
    Remove surrounding punctuation, including Greek-specific punctuation and dagger, from a token or lemma containing Greek characters.
    
    Args:
        token_or_lemma (str): The token or lemma from which surrounding punctuation and dagger are to be removed.
    
    Returns:
        str: The input string with surrounding punctuation and dagger removed, if present.
    """
    punctuation = string.punctuation + GREEK_ANO_TELEIA + GREEK_QUESTION_MARK + DAGGER + EM_DASH
    pattern = r'^([' + re.escape(punctuation) + r']+)?(.*[\u0370-\u03ff\u1f00-\u1fff]+)([' + re.escape(punctuation) + r']+)?$'
    match = re.match(pattern, token_or_lemma)
    if match:
        return match.group(2)  # Return the part with Greek characters, excluding surrounding punctuation/dagger/em dash
    return token_or_lemma
