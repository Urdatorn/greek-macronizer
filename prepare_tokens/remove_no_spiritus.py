'''
Removing lines with tokens 
    i) starting on a vowel and 
    ii) lacking spiritus on any character

An example line from the tokens is:
ὰ	a-p---na-	ὰ
'''

# Append the root folder to sys.path to be able to import from /utils.py
# Assuming your script is in a subfolder one level deep from the root
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import re
from utils import Colors, with_spiritus, all_vowels

def check_and_return_word(word):
    """
    Checks if the first character of the word is a vowel and
    if the word does not contain any characters with spiritus.
    """
    if re.match(all_vowels, word[0]) and not re.search(with_spiritus, word):
        return True  # The word meets the criteria for removal
    return False  # The word does not meet the criteria for removal

def process_tsv_file(input_file_path, output_file_path):
    """
    Processes a TSV file, removing lines whose first column starts with a vowel and
    completely lacks characters with spiritus. Prints the number of lines removed.
    """
    lines_removed = 0
    with open(input_file_path, 'r', encoding='utf-8') as infile, \
         open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Assuming the first column is the word to check
            first_column = line.strip().split('\t')[0]
            # Use the check_and_return_word function to determine if the line should be removed
            if check_and_return_word(first_column):
                lines_removed += 1  # Increment counter if the line meets the criteria and is to be removed
                print(line)
            else:
                # If the word does not meet the criteria for removal, it's written to the output file
                outfile.write(line)

    print(f"{Colors.RED}Total lines removed: {lines_removed}{Colors.ENDC}")

# Example usage
if __name__ == "__main__":
    test_words = ["ὰ", "ἀνθρωπος", "εὕρηκα", "ἐν", "κα"]  # A mix of words that do and do not meet the criteria
    for word in test_words:
        result = check_and_return_word(word)
        if result:
            print(f"Word '{word}' meets the criteria.")
        else:
            print(f"Word '{word}' does not meet the criteria.")

