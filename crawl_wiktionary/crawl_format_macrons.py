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
from greek_accentuation.characters import length, strip_length, base
from utils import base_alphabet, only_bases

SHORT = '̆'
LONG = '̄'

# Define length_count as a global dictionary
length_count = {'long': 0, 'short': 0}

print("Only bases: " + only_bases('ᾰ̓ᾱ́ᾰτᾰ'))


def process_word(word):
    '''
    >>process_word('νεᾱνῐ́ᾱς')
    >>('νεανίας', ['_3', '^5', '_6'])
    '''
    global length_count  # Declare length_count as global to modify it
    processed_word = ""
    modifications = []
    i = 1  # Initialize character position counter
    for char in word:
        if re.search(base_alphabet, base(char)):
            #print(f"{i}: {char}")
            char_length = length(char)
            if char_length == LONG:
                #print(char)
                processed_char = strip_length(char)
                modifications.append(f"_{i}")
                length_count['long'] += 1
            elif char_length == SHORT:
                #print(char)
                processed_char = strip_length(char)
                modifications.append(f"^{i}")
                length_count['short'] += 1
            else:
                processed_char = char

            processed_word += processed_char
            if char != SHORT and char != LONG:
                i += 1

    return processed_word, modifications

print(f"{process_word('ᾰ̓ᾱ́ᾰτᾰ')[1]}")

def process_file(input_file_path, output_file_path):
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

def main():
    parser = argparse.ArgumentParser(description='Modify polytonic Greek words to handle macrons and breves, appending markers and their positions to the tag column.')
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', required=True, help='Output file path')
    args = parser.parse_args()

    process_file(args.input, args.output)

if __name__ == "__main__":
    main()