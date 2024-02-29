"""
/prepare_tokens/remove_punctuation.py

To be called from /prepare_tokens/main_tokens.py

Processes text files to remove specified accents and punctuation from tokens and lemmas. It uses regex to target
accents and punctuation defined in ACCENTS and the Punctuation class from utils.py. The script removes these 
characters if they appear alone at the start or end of tokens and lemmas.

Workflow:
1. Constructs a regex pattern from ACCENTS and Punctuation.
2. Applies this pattern to remove unwanted characters from each token and lemma.
3. Reads from an input file, processes specified columns, and writes to an output file.

Intended for cleaning data in text processing tasks, enhancing data quality for further analysis or NLP workflows.

Usage:
Run with --input for the source file path and --output for the destination file path. 
"""

# IMPORTS

# Append the root folder to sys.path to be able to import from /utils.py
# Assuming your script is in a subfolder one level deep from the root
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re
import argparse
from tqdm import tqdm

from utils import Colors, Punctuation, Elision, ACCENTS

# DEFINITIONS

def construct_elision_regex():
    """
    Construct a regex pattern to match Elision signs at the beginning of a string.
    """
    elision_chars = [Elision.ELISION1, Elision.ELISION2]
    pattern = f"^({'|'.join(re.escape(el) for el in elision_chars)})"
    return pattern

def construct_accents_regex():
    """
    Construct a regex pattern for ACCENTS to match at the beginning or end of a string.
    """
    accents_pattern = f"({'|'.join(re.escape(acc) for acc in ACCENTS)})"
    return f"^{accents_pattern}+|{accents_pattern}+$"

def remove_accents_and_elision(token):
    """
    Remove specified ACCENTS from the start or end of a token and Elision signs from the start.
    Returns the cleaned token and the count of removed characters.
    """
    initial_length = len(token)
    elision_pattern = construct_elision_regex()
    accents_pattern = construct_accents_regex()
    # Remove Elision signs from the beginning
    token = re.sub(elision_pattern, '', token, flags=re.UNICODE)
    # Remove ACCENTS from the start or end
    token = re.sub(accents_pattern, '', token, flags=re.UNICODE)
    final_length = len(token)
    removed_count = initial_length - final_length
    return token, removed_count

def remove_punctuation(token):
    """
    Remove Punctuation defined in the Punctuation class from utils.py from anywhere in the token.
    Returns the cleaned token and the count of removed characters.
    """
    initial_length = len(token)
    for punct in dir(Punctuation):
        if not punct.startswith("__"):
            token = token.replace(getattr(Punctuation, punct), '')
    final_length = len(token)
    removed_count = initial_length - final_length
    return token, removed_count

def process_file(input_file_path, output_file_path):
    """
    Process each line of the input file, removing specified punctuation and accents
    from the first and third columns (TOKEN and LEMMA). Utilizes tqdm for progress
    indication. Also, prints the total number of punctuation characters removed.
    """
    punctuation_removed_count = 0
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            total_lines = sum(1 for _ in file)
        
        with open(input_file_path, 'r', encoding='utf-8') as input_file, \
             open(output_file_path, 'w', encoding='utf-8') as output_file:
            
            progress_bar = tqdm(total=total_lines, desc="Processing", unit="line", leave=True)
            
            for line in input_file:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    # Process TOKEN and LEMMA columns for ACCENTS, Elision, and Punctuation
                    token, token_removed = remove_accents_and_elision(parts[0])
                    lemma, lemma_removed = remove_accents_and_elision(parts[2])
                    parts[0], removed_count = remove_punctuation(token)
                    parts[2], lemma_count_removed = remove_punctuation(lemma)
                    punctuation_removed_count += token_removed + lemma_removed + removed_count + lemma_count_removed
                    output_file.write('\t'.join(parts) + '\n')
                
                progress_bar.update(1)
            
            progress_bar.close()

        print(f"{Colors.GREEN}Total punctuation characters removed: {punctuation_removed_count}{Colors.ENDC}")
        print(f"{Colors.GREEN}Processed content saved to: {output_file_path}{Colors.ENDC}")
    except FileNotFoundError:
        print(f"{Colors.RED}Error: The file {input_file_path} was not found.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}An unexpected error occurred: {e}{Colors.ENDC}")

def main():
    parser = argparse.ArgumentParser(description='Remove punctuation and accents from specific fields in a text file, with progress indication.')
    parser.add_argument('--input', type=str, help='Input file path', required=True)
    parser.add_argument('--output', type=str, help='Output file path', required=True)
    args = parser.parse_args()

    process_file(args.input, args.output)

if __name__ == "__main__":
    main()
