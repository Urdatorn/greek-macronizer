'''
Ta bort alla rader vars TOKEN
    - ej innehåller DICHRONA
    - har DICHRONA vars längder ges direkt av accentreglerna:
        - har cirkumflex på sin enda DICHRONA
        - är properispomenon och inte har DICHRONA på en tidigare stavelse än penultiman (behövs ej dictionary)

NB:
OXYTONE implies nothing without context (cf. αἰδώς)
PAROXYTONE with ≥3 syllables still does NOT imply long vowel in ultima, because not all accents are recessive (cf. pf. ppc. λελῠμένος)
PROPAROXYTONE implies that the vowel in the ultima is short
PERISPOMENON implies that the vowel in the ultima is long (as all vowels with circumf.)
PROPERISPOMENON implies that the vowel in the ultima is short

Usage:
    The script requires three command-line arguments:
    - `--input`: The path to the input file containing the text in Beta Code.
    - `--output`: The path where the non-aberrant lines will be written.
    - `--aberrant`: The path for the file where aberrant lines are saved.
'''
import csv
import argparse
from utils import Colors, DICHRONA


from greek_accentuation.syllabify import is_diphthong


def is_aberrant_token(token):
    """
    Determines if a token is aberrant based on specific criteria:
    - Does not contain A, I, or E (DICHRONA)
    - Is properispomenon and does not have DICHRONA before the second-to-last vowel group.
    """


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