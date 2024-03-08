# IMPORTS

# Append the root folder to sys.path to be able to import from /utils.py
# Assuming your script is in a subfolder one level deep from the root
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
import argparse
import re # for the regex patterns

# third-party imports
#from greek_accentuation.accentuation import get_accent_type, PROPERISPOMENON, PROPAROXYTONE
#from greek_accentuation.syllabify import ultima

# local imports
from utils import Colors, DICHRONA # /utils.py
from erics_syllabifier import patterns # /prepare_tokens/patterns.py
from erics_syllabifier import syllabifier

# END OF IMPORTS

'''
Since I scrapped the greek_accentuation package, I first need to define my own accentuation-word-class tools:
ultima()
properispomenon()
proparoxytone()

'''

### BASIC DEFINITIONS ###
# ultima
# properispomenon
# proparoxytone

def ultima(word):
    '''
    >> ultima('ποτιδέρκομαι')
    >> μαι
    '''
    list_of_syllables = syllabifier(word)
    ultima = list_of_syllables[-1]

    return ultima

def properispomenon(word):
    '''
    >> properispomenon('ὗσον')
    >> True
    '''
    list_of_syllables = syllabifier(word)
    if len(list_of_syllables) >= 2: 
        penultima = list_of_syllables[-2]
        circumflexes = r'[ᾶῆῖῦῶἇἆἦἧἶἷὖὗὦὧἦἧἆἇὧὦᾆᾇᾷᾖᾗᾦᾧῷῇ]'
        if re.search(circumflexes, penultima):
            return True
        else:
            return False
    else:
        return False

def proparoxytone(word):
    '''
    >> proparoxytone('ποτιδέρκομαι')
    >> True
    '''
    list_of_syllables = syllabifier(word)
    if len(list_of_syllables) >= 3: 
        antepenultima = list_of_syllables[-3]
        acutes = r'[άέήόίύώἄἅἔἕὄὅἤἥἴἵὔὕὤὥΐΰᾄᾅᾴᾔᾕῄᾤᾥῴ]'
        if re.search(acutes, antepenultima):
            return True
        else:
            return False
    else:
        return False



### AUXILIARY FUNCTIONS ###
#   is_diphthong
#   has_iota_subscriptum
#   has_iota_adscriptum
#   word_with_real_dichrona
#   properispomenon_with_dichronon_only_in_ultima
#   proparoxytone_with_dichronon_only_in_ultima

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
    - bool: True if the string contains a necessary DICHRONA character; 
            False otherwise.
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
            return True

    # If the loop completes without returning True, no necessary DICHRONA character was found
    return False

def properispomenon_with_dichronon_only_in_ultima(string):
    """
    Determines if a given string satisfies the following simplified criteria:
    - The entire string is recognized by `word_with_real_dichrona`.
    - The accent type of the string is classified as properispomenon.
    - The ultima of the string is recognized by `word_with_real_dichrona`.
    - The part of the string before the ultima is NO recognized by `word_with_real_dichrona`.
    
    The design importantly returns a word such as αὖθις.
    
    Parameters:
    - string (str): The input string to be evaluated.

    Returns:
    - bool: True if the string satisfies all specified conditions; otherwise, False.
    """
    # Check if the entire string is a word_with_real_dichrona
    if not word_with_real_dichrona(string):
        return False

    # Check if the accent type of the string is properispomenon
    if not properispomenon(string):
        return False
    
    # Extract the ultima of the string
    ultima_str = ultima(string)

    # Ensure the ultima itself is recognized by `word_with_real_dichrona`
    if not word_with_real_dichrona(ultima_str):
        return False

    # Determine the part of the string before the ultima
    pre_ultima = string[:-len(ultima_str)]

    # Ensure the part before the ultima is not recognized by `word_with_real_dichrona`
    # The pre_ultima conjunct checks whether the string is non-empty
    if pre_ultima and word_with_real_dichrona(pre_ultima):
        return False

    return True

def proparoxytone_with_dichronon_only_in_ultima(string):
    """
    Determines if a given string satisfies the following criteria:
    - The entire string is recognized by `word_with_real_dichrona` as containing a real dichrona.
    - The accent type of the string is classified as proparoxytone.
    - The ultima of the string is recognized by `word_with_real_dichrona`.
    - The part of the string before the ultima is not recognized by `word_with_real_dichrona`.

    Parameters:
    - string (str): The input string to be evaluated.

    Returns:
    - bool: True if the string satisfies all specified conditions; otherwise, False.
    """
    # Check if the entire string is a word_with_real_dichrona
    if not word_with_real_dichrona(string):
        return False

    # Check if the accent type of the string is PROPAROXYTONE
    if not proparoxytone(string):
        return False
    
    # Extract the ultima of the string
    ultima_str = ultima(string)

    # Ensure the ultima itself is recognized by `word_with_real_dichrona`
    if not word_with_real_dichrona(ultima_str):
        return False

    # Determine the part of the string before the ultima
    pre_ultima = string[:-len(ultima_str)]

    # Ensure the part before the ultima is not recognized by `word_with_real_dichrona`
    if pre_ultima and word_with_real_dichrona(pre_ultima):
        return False

    return True

### THE FILTER FUNCTION ###

def filter_dichrona(input_file_path):
    """
    Filters lines from a tab-separated input file based on three criteria related to dichrona tokens:
    - The token must be identified by `word_with_real_dichrona` as containing a real dichrona.
    - The token must not be identified by `properispomenon_with_dichronon_only_in_ultima`.
    - The token must not be identified by `proparoxytone_with_dichronon_only_in_ultima`.
    
    Tokens meeting all these criteria are put into the output_lines list and returned. 
    Tokens that fail any one of the criteria are considered filtered out and written to a separate filtered_out_lines list.
    
    Parameters:
    - input_file_path (str): Path to the input TSV file.
    """
    output_lines = []
    filtered_out_lines = []

    try:
        with open(input_file_path, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile, delimiter='\t')

            for row in reader:
                if row is None or not row:
                    continue

                token = row[0]
                print(token)

                # Apply criteria
                word_check = word_with_real_dichrona(token)
                print(word_check)
                prop_check = properispomenon_with_dichronon_only_in_ultima(token)
                print(prop_check)
                propoxy_check = proparoxytone_with_dichronon_only_in_ultima(token)
                print(propoxy_check)

                if word_check and not prop_check and not propoxy_check:
                    output_lines.append(row)
                else:
                    filtered_out_lines.append(row)

    except Exception as e:
        print(f"{Colors.RED}Error occurred: {e}{Colors.ENDC}")

    return output_lines, filtered_out_lines


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

print(ultima('πατρός')) # τρός, it sees muta cum liquida as single
print(ultima('ποτιδέρκομαι')) #
print(ultima('ὅττι')) # 
print(ultima('τλὰς')) # 

print(f'Example of properispomenon_with_dichronon_only_in_ultima:')
print(properispomenon_with_dichronon_only_in_ultima('ἀπῦσαν')) # False (nonsense word)
print(proparoxytone_with_dichronon_only_in_ultima('ἀπέπεπαν')) # False (nonsense word)
print(properispomenon_with_dichronon_only_in_ultima('αὖθις')) # True!!! :)
print(proparoxytone_with_dichronon_only_in_ultima('αἰπέπεπαν')) # True!!!

#debug = proparoxytone_with_dichronon_only_in_ultima('α')
#print(debug)

#print(filter_dichrona('prepare_tokens/tokens/test_filter.txt', 'prepare_tokens/tokens/test_filter_output.txt', 'prepare_tokens/tokens/test_filter_filtered.txt'))

from erics_syllabifier import syllabifier

def properispomenon(word):
    '''
    >> properispomenon('ὗσον')
    >> True
    '''
    list_of_syllables = syllabifier(word)
    if len(list_of_syllables) >= 2: 
        penultima = list_of_syllables[-2]
        circumflexes = r'[ᾶῆῖῦῶἇἆἦἧἶἷὖὗὦὧἦἧἆἇὧὦᾆᾇᾷᾖᾗᾦᾧῷῇ]'
        if re.search(circumflexes, penultima):
            return True
        else:
            return False
    else:
        return False
    
print(properispomenon('ὗσον'))

def proparoxytone(word):
    '''
    >> proparoxytone('ποτιδέρκομαι')
    >> True
    '''
    list_of_syllables = syllabifier(word)
    if len(list_of_syllables) >= 3: 
        antepenultima = list_of_syllables[-3]
        acutes = r'[άέήόίύώἄἅἔἕὄὅἤἥἴἵὔὕὤὥΐΰᾄᾅᾴᾔᾕῄᾤᾥῴ]'
        if re.search(acutes, antepenultima):
            return True
        else:
            return False
    else:
        return False

print(proparoxytone('ποτιδέρκομαι'))