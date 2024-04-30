'''
Format the crawled LSJ macrons, e.g. 

    πλάτας	n-p---fa-	πλάτη	πλᾰ́τας

and turn them into the likes of

    πλάτας	n-p---fa-	πλάτη	^3

The logic is exactly the same as in the Wiktionary crawl_format_macrons.py, and so can be reused.

'''

import csv

def filter_non_empty_fourth_column(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8', newline='') as infile, \
         open(output_file_path, 'w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        # Iterate through each line in the input TSV
        for line in reader:
            # Check if the line has at least four columns and the fourth column is not empty
            if len(line) >= 4 and line[3].strip():
                # Write the line to the output file if the fourth column is non-empty
                writer.writerow(line)


### crawl_format_macrons logic adapted to a four-column tsv input 

import re
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from greek_accentuation.characters import length, base

from utils import base_alphabet
from macrons_map import macrons_map

SHORT = '̆'
LONG = '̄'

# Define length_count as a global dictionary
length_count = {'long': 0, 'short': 0}


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
    global length_count  # Declare length_count as global to modify it
    modifications = []
    i = 1  # Initialize character position counter
    for char in word:
        if re.search(base_alphabet, base(char)):
            char_length = length(char)
            if char_length == LONG:
                modifications.append(f"_{i}")
                length_count['long'] += 1
            elif char_length == SHORT:
                modifications.append(f"^{i}")
                length_count['short'] += 1
            i += 1  # Only increment for non-length marking characters

    # Now strip all length diacritics after processing for position markings
    processed_word = strip_length_string(word)
    return processed_word, modifications


def process_file(input_file_path, output_file_path):
    '''
    Processes the entire file and applies modifications to each word in the fourth column,
    overwriting the fourth column with the vowel-length markings and ensuring each line has exactly five columns.
    '''
    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file, \
             open(output_file_path, 'w', encoding='utf-8') as output_file:
            for line in input_file:
                parts = line.strip().split('\t')
                
                # Ensure there are enough columns, pad if necessary
                while len(parts) < 5:
                    parts.append('')

                # Process only the fourth column if it exists
                if len(parts) >= 4:
                    # Get modifications for the fourth column
                    processed_word, modifications = process_word(parts[3])
                    # Replace the fourth column with the modifications
                    parts[3] = ''.join(modifications)

                # Write the updated line back to the output file
                output_file.write('\t'.join(parts) + '\n')
                
        print(f"Processing complete. Output saved to: {output_file_path}")
        print(f"Total macrons (long) stripped: {length_count['long']}")
        print(f"Total breves (short) stripped: {length_count['short']}")
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


input_file_path = 'crawl_lsj/macrons_lsj_raw_old_filter.tsv'
output_file_path = 'crawl_lsj/macrons_lsj.tsv'

#filter_non_empty_fourth_column(input_file_path, output_file_path)

process_file(input_file_path, output_file_path)