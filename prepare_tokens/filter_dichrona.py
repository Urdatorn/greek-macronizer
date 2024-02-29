'''
Filter out all lines with TOKENs (first column of tokens text file) which
    - ej innehåller DICHRONA
    - har DICHRONA vars längder ges direkt av accentreglerna:
        - har cirkumflex på sin enda DICHRONA
        - är properispomenon och inte har DICHRONA på en tidigare stavelse än penultiman (behövs ej dictionary)

NB:
OXYTONE implies nothing without context (cf. αἰδώς)
PAROXYTONE with ≥3 syllables still does NOT imply long vowel in ultima, because not all accents are recessive (cf. pf. ppc. λελῠμένος)
PROPAROXYTONE implies that the vowel in the ultima is short, except for the πόλις declination's εως, which however has no DICHRONA.
PERISPOMENON implies that the vowel in the ultima is long (as all vowels with circumf.)
PROPERISPOMENON implies that the vowel in the ultima is short

Usage:
    The script requires three command-line arguments:
    - `--input`: The path to the input file containing the text in Beta Code.
    - `--output`: The path where the non-aberrant lines will be written.
    - `--aberrant`: The path for the file where aberrant lines are saved.
'''

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
from greek_accentuation.accentuation import get_accent_type, PROPERISPOMENON, PROPAROXYTONE
from greek_accentuation.syllabify import ultima

# local imports
from utils import Colors, DICHRONA # /utils.py
from patterns import patterns # /prepare_tokens/patterns.py

# END OF IMPORTS

### 6 AUXILIARY DEFINITIONS ###
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
    - The accent type of the string is classified as PROPERISPOMENON.
    - The ultima of the string is recognized by `word_with_real_dichrona`.
    - The part of the string before the ultima is not recognized by `word_with_real_dichrona`.
    
    The design importantly returns a word such as αὖθις.
    
    Parameters:
    - string (str): The input string to be evaluated.

    Returns:
    - bool: True if the string satisfies all specified conditions; otherwise, False.
    """
    # Check if the entire string is a word_with_real_dichrona
    if not word_with_real_dichrona(string):
        return False

    # Check if the accent type of the string is PROPERISPOMENON
    if get_accent_type(string) != PROPERISPOMENON:
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

def proparoxytone_with_dichronon_only_in_ultima(string):
    """
    Determines if a given string satisfies the following criteria:
    - The entire string is recognized by `word_with_real_dichrona` as containing a real dichrona.
    - The accent type of the string is classified as PROPAROXYTONE.
    - The ultima of the string is recognized by `word_with_real_dichrona`.
    - The part of the string before the ultima is not recognized by `word_with_real_dichrona`.

    This function specifically identifies words that are accented as proparoxytone
    with the dichronon character exclusively present in the word's ultima, emphasizing
    a significant phonetic or morphological feature in that position.

    Parameters:
    - string (str): The input string to be evaluated.

    Returns:
    - bool: True if the string satisfies all specified conditions; otherwise, False.
    """
    # Check if the entire string is a word_with_real_dichrona
    if not word_with_real_dichrona(string):
        return False

    # Check if the accent type of the string is PROPAROXYTONE
    if get_accent_type(string) != PROPAROXYTONE:
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

# def filter_dichrona(input_file_path, output_file_path, filtered_out_file_path):
#     """
#     Filters lines from a tab-separated input file based on three criteria related to dichrona tokens:
#     - The token must be identified by `word_with_real_dichrona` as containing a real dichrona.
#     - The token must not be identified by `properispomenon_with_dichronon_only_in_ultima`.
#     - The token must not be identified by `proparoxytone_with_dichronon_only_in_ultima`.
    
#     Tokens meeting all these criteria are written to the output file for undecided dichrona tokens. 
#     Tokens that fail any one of the criteria are considered filtered out and written to a separate file.
    
#     Parameters:
#     - input_file_path (str): Path to the input TSV file.
#     - output_file_path (str): Path to the output TSV file for tokens meeting the criteria.
#     - filtered_out_file_path (str): Path to the output TSV file for tokens that are filtered out.
#     """
#     try:
#         with open(input_file_path, 'r', encoding='utf-8') as infile, \
#              open(output_file_path, 'w', newline='', encoding='utf-8') as outfile, \
#              open(filtered_out_file_path, 'w', newline='', encoding='utf-8') as filtered_outfile:

#             reader = csv.reader(infile, delimiter='\t')
#             output_writer = csv.writer(outfile, delimiter='\t')
#             filtered_out_writer = csv.writer(filtered_outfile, delimiter='\t')

#             total_input_lines, total_output_lines, total_filtered_out_lines = 0, 0, 0

#             for row in reader:
#                 total_input_lines += 1
#                 token = row[0]
                
#                 # Assuming word_with_real_dichrona, properispomenon_with_dichronon_only_in_ultima,
#                 # and proparoxytone_with_dichronon_only_in_ultima are implemented elsewhere
#                 if word_with_real_dichrona(token) and not properispomenon_with_dichronon_only_in_ultima(token) \
#                    and not proparoxytone_with_dichronon_only_in_ultima(token):
#                     output_writer.writerow(row)
#                     total_output_lines += 1
#                 else:
#                     filtered_out_writer.writerow(row)
#                     total_filtered_out_lines += 1

#             # Print summary
#             print(f"{Colors.GREEN}Total number of input lines: {total_input_lines}{Colors.ENDC}")
#             print(f"{Colors.RED}Total number of lines written to the output file: {total_output_lines}{Colors.ENDC}")
#             print(f"{Colors.RED}Total number of filtered-out lines: {total_filtered_out_lines}{Colors.ENDC}")
#             print(f"{Colors.GREEN}Output file path: {output_file_path}{Colors.ENDC}")
#             print(f"{Colors.GREEN}Filtered out file path: {filtered_out_file_path}{Colors.ENDC}")

#     except Exception as e:
#         print(f"{Colors.RED}Error occurred: {e}{Colors.ENDC}")

def filter_dichrona(input_file_path, output_file_path, filtered_out_file_path):
    """
    Filters lines from a tab-separated input file based on three criteria related to dichrona tokens:
    - The token must be identified by `word_with_real_dichrona` as containing a real dichrona.
    - The token must not be identified by `properispomenon_with_dichronon_only_in_ultima`.
    - The token must not be identified by `proparoxytone_with_dichronon_only_in_ultima`.
    
    Tokens meeting all these criteria are written to the output file for undecided dichrona tokens. 
    Tokens that fail any one of the criteria are considered filtered out and written to a separate file.
    
    Parameters:
    - input_file_path (str): Path to the input TSV file.
    - output_file_path (str): Path to the output TSV file for tokens meeting the criteria.
    - filtered_out_file_path (str): Path to the output TSV file for tokens that are filtered out.
    """
    try:
        with open(input_file_path, 'r', encoding='utf-8') as infile, \
             open(output_file_path, 'w', newline='', encoding='utf-8') as outfile, \
             open(filtered_out_file_path, 'w', newline='', encoding='utf-8') as filtered_outfile:

            reader = csv.reader(infile, delimiter='\t')
            output_writer = csv.writer(outfile, delimiter='\t')
            filtered_out_writer = csv.writer(filtered_outfile, delimiter='\t')

            total_input_lines, total_output_lines, total_filtered_out_lines = 0, 0, 0

            for row in reader:
                if row is None:
                    print(f"{Colors.YELLOW}Warning: Encountered None row.{Colors.ENDC}")
                    continue
                if not row:
                    print(f"{Colors.YELLOW}Warning: Encountered empty row.{Colors.ENDC}")
                    continue

                total_input_lines += 1
                token = row[0]

                # Debugging print to ensure token is not None
                if token is None:
                    print(f"{Colors.YELLOW}Warning: Token is None in row: {row}{Colors.ENDC}")
                    continue

                # Assuming the necessary functions return True/False and are implemented elsewhere
                word_check = word_with_real_dichrona(token)
                prop_check = properispomenon_with_dichronon_only_in_ultima(token)
                propoxy_check = proparoxytone_with_dichronon_only_in_ultima(token)
                
                # Debugging prints for function returns
                print(f"Debug: Token '{token}', word_check: {word_check}, prop_check: {prop_check}, propoxy_check: {propoxy_check}")

                if word_check and not prop_check and not propoxy_check:
                    output_writer.writerow(row)
                    total_output_lines += 1
                else:
                    filtered_out_writer.writerow(row)
                    total_filtered_out_lines += 1

            # Print summary
            print(f"{Colors.GREEN}Total number of input lines: {total_input_lines}{Colors.ENDC}")
            print(f"{Colors.RED}Total number of lines written to the output file: {total_output_lines}{Colors.ENDC}")
            print(f"{Colors.RED}Total number of filtered-out lines: {total_filtered_out_lines}{Colors.ENDC}")
            print(f"{Colors.GREEN}Output file path: {output_file_path}{Colors.ENDC}")
            print(f"{Colors.GREEN}Filtered out file path: {filtered_out_file_path}{Colors.ENDC}")

    except Exception as e:
        print(f"{Colors.RED}Error occurred: {e}{Colors.ENDC}")

### MAIN ###

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Identify aberrant lines based on Beta Code in a text file.')
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', required=True, help='Output file path for lines with undecided dichrona')
    parser.add_argument('--filtered_out', required=True, help='File path to write filtered-out lines to')
    args = parser.parse_args()

    filter_dichrona(args.input, args.output, args.aberrant)