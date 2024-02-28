'''
Remember, unicode normalization changes oxeia to tonos,
but our normalization and cltk does the inverse.

cltk does not cover the two diaeresis/trema/dialytika cases, so I've updated the dictionary
from TONOS_OXIA to TONOS_OXIA_PLUS_DIALYTIKA to be explicit, and hence updated the functions as well.
'''

import csv
from utils import Colors  # Make sure utils.py is in the same directory or its path is added to PYTHONPATH

TONOS_OXIA_PLUS_DIALYTIKA = {
    '\u03ac': '\u1f71', # ά
    '\u03ad': '\u1f73', # έ
    '\u03ae': '\u1f75', # ή
    '\u03af': '\u1f77', # ί
    '\u03cc': '\u1f79', # ό
    '\u03cd': '\u1f7b', # ύ
    '\u03ce': '\u1f7d', # ώ
    '\u0390': '\u1fd3', # ΐ Greek Small Letter Iota With Dialytika And Oxia; my addition
    '\u03b0': '\u1fe3', # ΰ Greek Small Letter Iota With Dialytika And Oxia; my addition
}

def tonos_oxia_converter(text, reverse=False):
    """cltk's version with added dialytika. Without this
    normalization, string comparisons will fail."""
    for char_tonos, char_oxia in TONOS_OXIA_PLUS_DIALYTIKA.items():
        if not reverse:
            text = text.replace(char_tonos, char_oxia)
        else:
            text = text.replace(char_oxia, char_tonos)
    return text

# actually normalizing an input file starts here

def normalize_columns(input_file_path, output_file_path):
    """
    Normalize the first and third columns of a tabulated text file using tonos_oxia_converter
    and keep track of how many characters were changed, including their Unicode escape codes and characters,
    and how many of each category were changed.
    """
    changed_characters_count = 0
    character_change_counts = {key: 0 for key in TONOS_OXIA_PLUS_DIALYTIKA.keys()}  # Initialize counts for each character

    with open(input_file_path, 'r', encoding='utf-8') as infile, \
         open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        for row in reader:
            if len(row) >= 3:
                # Process the first column
                normalized_first, changes_first = process_column(row[0], character_change_counts)
                changed_characters_count += len(changes_first)

                # Process the third column
                normalized_third, changes_third = process_column(row[2], character_change_counts)
                changed_characters_count += len(changes_third)

                # Update row with normalized values
                row[0], row[2] = normalized_first, normalized_third

            writer.writerow(row)

    # Printing the results
    print(f"{Colors.GREEN}{changed_characters_count} characters were changed.{Colors.ENDC}")
    for original_char in TONOS_OXIA_PLUS_DIALYTIKA.keys():  # Ensure the original order is maintained
        changed_char = TONOS_OXIA_PLUS_DIALYTIKA[original_char]
        count = character_change_counts[original_char]
        if count > 0:
            print(f"\\u{ord(original_char):04x} ({original_char}) to \\u{ord(changed_char):04x} ({changed_char}): {count}")

def process_column(column_data, character_change_counts):
    """Normalize column data using tonos_oxia_converter and track changes."""
    normalized_data = tonos_oxia_converter(column_data)
    changes = []
    for a, b in zip(column_data, normalized_data):
        if a != b:
            character_change_counts[a] += 1  # Update the count for this character
            changes.append((a, b))
    return normalized_data, changes


def main():
    input_file_path = 'input_file.txt'  # Specify the path to your input file
    output_file_path = 'normalized_output.txt'  # Specify the path for the output file

    normalize_columns(input_file_path, output_file_path)

if __name__ == "__main__":
    main()