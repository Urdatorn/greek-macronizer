import sys
import os
import re
from greek_accentuation.accentuation import get_accent_type, PROPERISPOMENON, PROPAROXYTONE
from greek_accentuation.syllabify import ultima

# Append the root folder to sys.path
# Assuming your script is in a subfolder one level deep from the root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import DICHRONA
from patterns import patterns

def is_diphthong(chars):
    ''' Expects two characters '''
    # Check if the input matches either of the diphthong patterns
    for pattern in ['diphth_y', 'diphth_i']:
        if re.match(patterns[pattern], chars):
            return True
    return False

def has_iota_subscriptum(char):
    ''' Expects one character '''
    subscr_i_pattern = re.compile(patterns['subscr_i'])
    # Check if the character matches the subscript iota pattern
    if subscr_i_pattern.match(char):
        return True
    return False

def has_iota_adscriptum(chars):
    ''' Expects two characters '''
    adscr_i_pattern = re.compile(patterns['adscr_i'])
    # Check if the two-character string matches the adscript iota pattern
    if adscr_i_pattern.match(chars):
        return True
    return False

def word_with_real_dichrona(s):
    """
    Determines if a given string contains at least one character from the DICHRONA set 
    that does not form a diphthong with its neighboring character and does not have a 
    silent iota (either subscriptum or adscriptum).

    This function iterates through each character in the input string. For characters
    that are part of the DICHRONA set, it performs several checks:
    1. If the character itself is a subscript iota (has a silent iota subscriptum).
    2. If the character, along with its preceding or succeeding character, forms a diphthong.
    3. If the character, along with its preceding or succeeding character, has an iota adscriptum.

    This function evaluates each character in the string to determine if it meets the criteria
    for being considered a "real" dichrona character, which includes not forming a diphthong
    with adjacent characters and not having an iota subscriptum or adscriptum. The presence of
    such a character signifies the string as containing a "real" dichrona and thus is returned.

    Parameters:
    - s (str): The input string to be checked.

    Returns:
    - str or None: The original string if it contains a necessary DICHRONA character; 
                   None if no such character is found.
    """
    for i, char in enumerate(s):
        if char in DICHRONA:
            # Check for subscript iota since it applies to single characters
            if has_iota_subscriptum(char):
                continue  # This DICHRONA character does not meet the criteria

            # Form pairs to check for diphthongs and adscriptum
            prev_pair = s[i-1:i+1] if i > 0 else ''
            next_pair = s[i:i+2] if i < len(s) - 1 else ''

            # Check if the character is part of a diphthong or has adscriptum
            if (prev_pair and (is_diphthong(prev_pair) or has_iota_adscriptum(prev_pair))) or \
               (next_pair and (is_diphthong(next_pair) or has_iota_adscriptum(next_pair))):
                continue  # Skip if any of these conditions are true

            # If the character passes all checks, the string contains a necessary DICHRONA character
            return s

    # If the loop completes without returning, no necessary DICHRONA character was found
    return None

def properispomenon_with_dichronon_only_in_ultima(string):
    """
    Determines if a given string meets all of the following criteria:
    - Contains only one DICHRONA character.
    - The word is identified by `word_with_real_dichrona` as containing a real dichrona.
    - The accent type of the string is classified as PROPERISPOMENON.
    - The DICHRONA character is located only in the ultima (last syllable) of the string.

    This function is specifically designed to identify words that are accented as
    properispomenon and where the dichronon character, indicating a significant
    phonetic or morphological feature, is exclusively present in the word's ultima.

    Parameters:
    - string (str): The input string to be evaluated.

    Returns:
    - bool: True if the string satisfies all specified conditions; otherwise, False.
    """
    # Check if the string has only one DICHRONA
    dichrona_count = sum(1 for char in string if char in DICHRONA)
    if dichrona_count != 1:
        return False
    
    # Check if word_with_real_dichrona returns True for the string
    if not word_with_real_dichrona(string):
        return False
    
    # Check if the accent type of the string is PROPERISPOMENON
    if get_accent_type(string) != PROPERISPOMENON:
        return False
    
    # Check if the ultima is a word with a real dichrona
    ultima_string = ultima(string)
    if not word_with_real_dichrona(ultima_string):
        return False
    
    return True

def proparoxytone_with_dichronon_only_in_ultima(string):
    """
    Checks if the given string satisfies the following criteria:
    - Contains only one DICHRONA character.
    - Is identified by `word_with_real_dichrona` as containing a real dichrona.
    - Has an accent type classified as PROPAROXYTONE.
    - Has the DICHRONA character located only in the ultima (last syllable) of the string.

    This function specifically identifies words that are accented as proparoxytone
    with the dichronon character exclusively present in the word's ultima, indicating
    a significant phonetic or morphological feature in that position.

    Parameters:
    - string (str): The input string to be evaluated.

    Returns:
    - bool: True if the string satisfies all specified conditions; otherwise, False.
    """
    # Check if the string has only one DICHRONA
    dichrona_count = sum(1 for char in string if char in DICHRONA)
    if dichrona_count != 1:
        return False
    
    # Check if word_with_real_dichrona returns True for the string
    if not word_with_real_dichrona(string):
        return False
    
    # Check if the accent type of the string is PROPAROXYTONE
    if get_accent_type(string) != PROPAROXYTONE:
        return False
    
    # Check if the DICHRONA character is located only in the ultima
    ultima_string = ultima(string)
    if not word_with_real_dichrona(ultima_string) or all(char not in DICHRONA for char in ultima_string):
        return False
    
    return True


# Example diphthongs
print(is_diphthong("αὐ"))  # Should return True if matching diphth_y pattern
print(is_diphthong("εἰ"))  # Should return True if matching diphth_i pattern
print(is_diphthong("ασ"))  # Expected False, not a diphthong pattern
print(is_diphthong("ἄι"))  # Expected False, not a diphthong pattern

# Example iotas
print(has_iota_subscriptum("ᾳ"))  # Expected True for subscript iota
print(has_iota_adscriptum("ἀι"))  # Expected True for adscript iota
print(has_iota_subscriptum("α"))  # Expected False, no iota
print(has_iota_adscriptum("αἰ"))  # Expected False

print(f'Examples of is_necessary:')
print(word_with_real_dichrona("μακραί"))  # Return
print(word_with_real_dichrona("ἐλύθη"))  # Return
print(word_with_real_dichrona("αἰ"))  # None
print(word_with_real_dichrona("ἀι"))  # None
print(word_with_real_dichrona("νεφέλᾳ"))  # None

print(get_accent_type('ὗσον') == PROPERISPOMENON) # True. NB: get_accent_type returns the accent type of a word as a tuple of the syllable number and accent
print(ultima('πατρός')) # τρός, it sees muta cum liquida as single
print(ultima('ποτιδέρκομαι')) # μαι
print(ultima('ὅττι')) # μαι

print(properispomenon_with_dichronon_only_in_ultima('ὗσαν')) # True
print(proparoxytone_with_dichronon_only_in_ultima('πέπεπαν')) # True
print(properispomenon_with_dichronon_only_in_ultima('αὖθις')) # True
print(proparoxytone_with_dichronon_only_in_ultima('πέπεπαν')) # True