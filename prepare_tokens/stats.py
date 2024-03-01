# Append the root folder to sys.path to be able to import from /utils.py
# Assuming the script is in a subfolder one level deep from the root
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re

from utils import DICHRONA

def analyze_file(file_path):
    lines_count = 0
    unique_lemmas = set()
    dichrona_count = 0
    tokens_ending_with_apostrophe = 0
    tokens_capital_first_character = 0
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            lines_count += 1
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                token, _, lemma = parts[:3]
                
                unique_lemmas.add(lemma)
                
                if any(char in DICHRONA for char in token):
                    dichrona_count += 1
                
                if token.endswith("'"):
                    tokens_ending_with_apostrophe += 1
                
                if token[0].isupper():
                    tokens_capital_first_character += 1
    
    return {
        'lines': lines_count,
        'unique_lemmas': len(unique_lemmas),
        'dichrona_chars': dichrona_count,
        'tokens_ending_apostrophe': tokens_ending_with_apostrophe,
        'tokens_capital_first': tokens_capital_first_character,
    }

def write_stats(file_paths, output_file):
    with open(output_file, 'w', encoding='utf-8') as out:
        for file_path in file_paths:
            stats = analyze_file(file_path)
            
            stats_output = f"""
{file_path}
Number of lines: {stats['lines']}
Number of unique LEMMAs: {stats['unique_lemmas']}
Number of DICHRONA characters in the first columns: {stats['dichrona_chars']}
Number of TOKENs ending with ': {stats['tokens_ending_apostrophe']}
Number of TOKENs with a capital first character: {stats['tokens_capital_first']}
"""
            print(stats_output)
            out.write(stats_output + '\n')

def main():
    # List of file paths to analyze
    file_paths = ['file1.txt', 'file2.txt', 'file3.txt']
    
    # Output file path
    output_file = 'stats.txt'
    
    write_stats(file_paths, output_file)

if __name__ == '__main__':
    main()
