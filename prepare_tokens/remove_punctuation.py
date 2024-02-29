# IMPORTS

# Append the root folder to sys.path to be able to import from /utils.py
# Assuming your script is in a subfolder one level deep from the root
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import string
import unicodedata
import argparse
from utils import Colors, Punctuation

# Define accents to remove if found alone at the beginning or end
ACCENTS = [
    "\u0376", "\u0384", "\u0385", "\u0387", "\u1fbd", "\u1fbe", "\u1fbf", "\u1fc0",
    "\u1fc1", "\u1fcd", "\u1fce", "\u1fcf", "\u1fdd", "\u1fde", "\u1fdf", "\u1fed",
    "\u1fee", "\u1fef", "\u1ffd", "\u1ffe",
]

def remove_single_accents(s):
    """Remove accents if found alone at the beginning or end of the string."""
    for accent in ACCENTS:
        if s.startswith(accent) or s.endswith(accent):
            s = s.strip(accent)
    return s

def remove_elision(token, position):
    """Remove elision marks from the beginning of tokens or lemmas."""
    if position in [0, 2]:  # For TOKEN and LEMMA columns
        if token.startswith(Punctuation.ELISION1) or token.startswith(Punctuation.ELISION2):
            return token[1:]
    return token

def remove_punctuation_from_file(input_file_path, output_file_path):
    """Remove specified punctuation from the first and third columns of the input file."""
    punctuation = string.punctuation + ''.join(getattr(Punctuation, attr) for attr in dir(Punctuation) if not attr.startswith("__"))
    remove_punct_map = dict.fromkeys(map(ord, punctuation), None)

    punctuation_removed_count = 0

    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
            for line in input_file:
                parts = line.strip().split('\t')
                if len(parts) == 3:
                    for i in [0, 2]:  # Process TOKEN and LEMMA
                        parts[i] = remove_elision(parts[i], i)
                        original_len = len(parts[i])
                        parts[i] = remove_single_accents(parts[i].translate(remove_punct_map))
                        punctuation_removed_count += original_len - len(parts[i])
                    output_file.write('\t'.join(parts) + '\n')

        print(f"{Colors.GREEN}Processed content saved to: {output_file_path}{Colors.ENDC}")
        print(f"{Colors.RED}Total punctuation characters removed: {punctuation_removed_count}{Colors.ENDC}")
    except FileNotFoundError:
        print(f"{Colors.RED}Error: The file {input_file_path} was not found.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}An unexpected error occurred: {e}{Colors.ENDC}")

def main():
    parser = argparse.ArgumentParser(description='Remove punctuation from specific fields in a text file.')
    parser.add_argument('--input', type=str, help='Input file path', required=True)
    parser.add_argument('--output', type=str, help='Output file path', required=True)
    args = parser.parse_args()

    remove_punctuation_from_file(args.input, args.output)

if __name__ == "__main__":
    main()
