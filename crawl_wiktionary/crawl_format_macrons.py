'''
Takes a list of polytonic Greek tokens such as 

νεᾱνῐ́ᾱς
νεᾱνῐ́ᾳ
νεᾱνῐείᾱ
νεᾱνῐεύομαι

and separates the tokens from the vowel-lengths, turning it into a two-column TSV, such as

νεανίας	_3^5_6
'''
import re
import argparse
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
    Processes the entire file and applies modifications to each word.
    '''
    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file, \
             open(output_file_path, 'w', encoding='utf-8') as output_file:
            for line in input_file:
                parts = line.strip().split('\t')
                processed_word, modifications = process_word(parts[0])
                if len(parts) > 1:
                    parts[1] += ''.join(modifications)
                else:
                    parts.append(''.join(modifications))
                parts[0] = processed_word
                output_file.write('\t'.join(parts) + '\n')
        print(f"Processing complete. Output saved to: {output_file_path}")
        print(f"Total macrons (long) stripped: {length_count['long']}")
        print(f"Total breves (short) stripped: {length_count['short']}")
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


#process_file('crawl_wiktionary/macrons_wiktionary_test.txt','crawl_wiktionary/macrons_wiktionary_test_format.txt')


def main():
    parser = argparse.ArgumentParser(description='Modify polytonic Greek words to handle macrons and breves, appending markers and their positions to the tag column.')
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', required=True, help='Output file path')
    args = parser.parse_args()

    process_file(args.input, args.output)

if __name__ == "__main__":
    main()
