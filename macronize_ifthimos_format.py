'''
Convert the raw ifthimos macrons, i.e.
    Ἀγαβάτας	n-s---mn-	Ἀγαβάτας	Αααᾱ
or
    ἀγαθάς	a-p---fa-	ἀγαθός	ααᾱ,
into a line with proper macrons, i.e.
    ἀγαθάς	a-p---fa-	ἀγαθός	_6

The raw ifthimos macrons only use the following characters:
    ΑαιυᾱᾹῑῙῡῩ
(with only 37 iotas and 44 hypsilons against 3104 alphas.)

Only 3183 lines have macrons from ifthimos.


'''

import csv
import re

from greek_accentuation.characters import length, base

from utils import only_bases, base_alphabet
from crawl_wiktionary.macrons_map import macrons_map


LONG = '̄'

def strip_length_string(string):
    '''
    Strips the input string of all length diacritics using the macrons_map dictionary.
    >>> strip_length_string('ᾰᾸᾱᾹῐῘῑῙῠῨῡῩᾰ̓Ᾰ̓ᾰ̔Ᾰ̔ᾰ́ᾰ̀ᾱ̓Ᾱ̓ᾱ̔Ᾱ̔ᾱ́ᾱ̀ᾱͅῐ̓Ῐ̓ῐ̔Ῐ̔ῐ́ῐ̀ῐ̈ῑ̓Ῑ̓ῑ̔Ῑ̔ῑ́ῑ̈ῠ̓ῠ̔Ῠ̔ῠ́ῠ̀ῠ͂ῠ̈ῠ̒ῡ̔Ῡ̔ῡ́ῡ̈')
    >>> αΑαΑιΙιΙυΥυΥἀἈἁἉάὰἀἈἁἉάὰᾳἰἸἱἹίὶϊἰἸἱἹίϊὐὑὙύὺῦϋυ̒ὑὙύϋ
    '''
    for composite, replacement in macrons_map.items():
        string = string.replace(composite, replacement)
    return string


def process_word(word):
    '''
    Processes each word to identify vowel length markers and create a TSV format.
    '''
    
    modifications = []
    i = 1  # Initialize character position counter
    for char in word:
        if re.search(base_alphabet, base(char)):
            char_length = length(char)
            if char_length == LONG:
                modifications.append(f"_{i}")
            i += 1  # Only increment for non-length marking characters

    processed_word = strip_length_string(word)
    return processed_word, modifications


def placements_alpha(line):
    """
    Processes a given TSV line. If the base form of the fourth column contains the Greek letter alpha,
    process the word and return the 'placements' part of the result.
    
    Parameters:
    - line (str): A string representing a row from a TSV file, expected to be tab-separated.

    Returns:
    - placements (str): The processed placements information if conditions are met, otherwise None.
    """
    try:
        # Split the line into columns using the tab delimiter
        columns = line.split('\t')
        
        # Ensure the line has at least four elements
        if len(columns) < 4:
            return None
        
        # Process the fourth column to remove diacritics
        base_text = only_bases(columns[3])
        
        # Check if the processed text contains 'α'
        if 'α' in base_text:
            # Assuming process_word returns a tuple or list and we need the second element
            result = process_word(columns[3])
            if result and len(result) > 1:
                placements = result[1]
                return placements
            
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Example usage
example_line = 'ἀγαθάς	a-p---fa-	ἀγαθός	ααᾱ' # Sample data line
print(placements_alpha(example_line))


# Example usage
#input_file_path = 'macrons_ifthimos_raw.tsv'  # Replace 'input.tsv' with your actual input file path
#output_file_path = 'macrons_ifthimos_raw_filter.tsv'  # Replace 'output.tsv' with your desired output file path

