import unicodedata
from pyuca import Collator

def find_base_macron_combinations(input_file_path, output_file_path):
    # Define base macrons and combining marks
    base_macrons = {'ᾰ', 'Ᾰ', 'ᾱ', 'Ᾱ', 'ῐ', 'Ῐ', 'ῑ', 'Ῑ', 'ῠ', 'Ῠ', 'ῡ', 'Ῡ'}
    combining_codes = {
        '\u0301',  # COMBINING ACUTE ACCENT
        '\u0308',  # COMBINING DIAERESIS
        '\u035C',  # COMBINING DOUBLE BREVE BELOW
        '\u0300',  # COMBINING GRAVE ACCENT
        '\u0313',  # COMBINING COMMA ABOVE
        '\u032F',  # COMBINING INVERTED BREVE BELOW
        '\u0314',  # COMBINING REVERSED COMMA ABOVE
        '\u0312',  # COMBINING TURNED COMMA ABOVE
        '\u0345',  # COMBINING GREEK YPOGEGRAMMENI
        '\u0342',  # COMBINING GREEK PERISPOMENI
    }

    # Open the input file and read all its content
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    results = set()

    # Iterate over characters in the text
    for i in range(len(text) - 1):
        current_char = text[i]
        next_char = text[i + 1]
        
        # Check if current character is a base macron and the next is a combining mark
        if current_char in base_macrons and next_char in combining_codes:
            combined_character = current_char + next_char
            results.add(combined_character)

    # Sort the dictionary by the composite characters using pyuca Collator
    collator = Collator()
    sorted_results = sorted(results, key=lambda item: collator.sort_key(item))
    
    # Write results to the output Python file
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        outfile.write("combined_macrons_map = {\n")
        for char in sorted_results:
            # Decompose to show the parts
            decomposed = "+".join(hex(ord(part)) for part in char)
            name = " ".join(unicodedata.name(part, "UNKNOWN") for part in char)
            outfile.write(f"    '{decomposed}': '',  # {char}: {name}\n")
        outfile.write("}\n")

    print(f"All unique combinations written to {output_file_path}")

# Example usage
input_file_path = 'crawl_wiktionary/macrons_wiktionary_raw.txt'
output_file_path = 'combined_macrons_map.py'
find_base_macron_combinations(input_file_path, output_file_path)
