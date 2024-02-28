'''
Ta bort alla rader vars TOKEN
    - ej innehåller DICHRONA
    - har cirkumflex på sin enda α, ι, υ (i.e. bara en A, I, U och denna följs av = innan nästa bokstav)
    - är properispomenon och inte har α, ι, υ på en tidigare stavelse än penultiman (behövs ej dictionary)

Usage:
    The script requires three command-line arguments:
    - `--input`: The path to the input file containing the text in Beta Code.
    - `--output`: The path where the non-aberrant lines will be written.
    - `--aberrant`: The path for the file where aberrant lines are saved.
'''
import csv
import argparse

# Definitions
GREEK_ALPHABET = "ABGDEZHQIKLMNCOPRSTUFXYW"  # 'J' and 'V' are not used in BETA CODE
VOWELS = "AEHIOUW" # alpha, epsilon, eta, iota, omicron, ypsilon, omega
DICHRONA = "AIU" # alpha, iota and ypsilon
COMBINING_DIACRITICS = "()/=\\+|"  # Including U+007C for | (iota subscript) and + for ¨ (diaeresis). NB: When you want to include an actual backslash character in a string, you need to escape it by using two backslashes (\\), so Python understands you mean a literal backslash rather than the start of an escape sequence.
ACCENTS = "/=\\"
CIRCUMFLEX = "="

def consolidate_vowels(token):
    """
    Consolidates vowels in the token, considering a vowel followed by 'I' or 'U' as a single vowel group.
    Other vowels are not consolidated into groups unless followed by 'I' or 'U'.
    """
    vowels_positions = [i for i, char in enumerate(token) if char in VOWELS]
    consolidated_vowels = []

    i = 0
    while i < len(vowels_positions):
        if i < len(vowels_positions) - 1 and (token[vowels_positions[i] + 1] == 'I' or token[vowels_positions[i] + 1] == 'U'):
            # Vowel followed by 'I' or 'U', treat as a single group
            consolidated_vowels.append(vowels_positions[i])
            i += 2  # Skip the next character ('I' or 'U')
        else:
            consolidated_vowels.append(vowels_positions[i])
            i += 1

    return consolidated_vowels

def is_properispomenon(token):
    """
    Determines if a token is properispomenon by checking for a '=' among the combining diacritics
    following its second-to-last vowel, considering vowels followed by 'I' or 'U' as single groups.
    """
    consolidated_vowels = consolidate_vowels(token)
    if len(consolidated_vowels) < 2:
        return False

    second_to_last_vowel_pos = consolidated_vowels[-2]
    return '=' in token[second_to_last_vowel_pos + 1:]

def has_dichrona_before_second_to_last_vowel_group(token):
    """
    Checks if the token has DICHRONA before the second-to-last vowel group,
    considering vowels followed by 'I' or 'U' as single groups.
    """
    consolidated_vowels = consolidate_vowels(token)
    if len(consolidated_vowels) < 2:
        return False

    second_to_last_vowel_pos = consolidated_vowels[-2]
    return any(char in DICHRONA for char in token[:second_to_last_vowel_pos])

def is_aberrant_token(token):
    """
    Determines if a token is aberrant based on specific criteria:
    - Does not contain A, I, or E (DICHRONA)
    - Is properispomenon and does not have DICHRONA before the second-to-last vowel group.
    """
    if not any(char in DICHRONA for char in token):
        return True

    if is_properispomenon(token) and not has_dichrona_before_second_to_last_vowel_group(token):
        return True

    return False

def handle_aberrant_lines(input_file_path, output_file_path, aberrant_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file, \
             open(output_file_path, 'w', newline='', encoding='utf-8') as output_file, \
             open(aberrant_file_path, 'w', newline='', encoding='utf-8') as aberrant_file:

            reader = csv.reader(file, delimiter='\t')
            aberrant_lines = []
            non_aberrant_lines = []
            total_input_lines = 0

            for row in reader:
                total_input_lines += 1
                # Remove lines with less than 3 columns or has no undecided DICHRONA
                if len(row) != 3 or is_aberrant_token(row[0]):
                    aberrant_lines.append(row)
                else:
                    non_aberrant_lines.append(row)

            output_writer = csv.writer(output_file, delimiter='\t')
            output_writer.writerows(non_aberrant_lines)

            aberrant_writer = csv.writer(aberrant_file, delimiter='\t')
            aberrant_writer.writerows(aberrant_lines)

            print(f"Total number of input lines: {total_input_lines}")
            print(f"Total number of aberrant lines: {len(aberrant_lines)}")
            print(f"Aberrant lines saved to: {aberrant_file_path}")
            print(f"Non-aberrant lines saved to: {output_file_path}")

    except FileNotFoundError as e:
        print(f"File not found error: {e.filename}. Please ensure the file exists and try again.")
        # Optionally, you can exit the script or continue to the next operation.
        return  # Exit the function early

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Handle or log the unexpected error and optionally exit
        return  # Exit on unexpected error

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Identify aberrant lines based on Beta Code in a text file.')
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', required=True, help='Output file path for non-aberrant lines')
    parser.add_argument('--aberrant', required=True, help='File path to write aberrant lines')
    args = parser.parse_args()

    handle_aberrant_lines(args.input, args.output, args.aberrant)