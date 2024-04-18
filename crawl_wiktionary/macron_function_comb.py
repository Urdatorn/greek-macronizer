import re
import unicodedata
from pyuca import Collator

def replace_composites(input_file_path, output_file_path, macron_map):
    # Define the characters that are of interest
    base_macrons = set(macron_map.keys())
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
    
    collator = Collator()

    with open(input_file_path, 'r', encoding='utf-8') as infile, \
         open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            new_line = []
            i = 0
            while i < len(line):
                char = line[i]
                next_char = line[i+1] if i+1 < len(line) else ''
                
                if next_char and (char + next_char in base_macrons):
                    if (unicodedata.decomposition(next_char) or next_char) in combining_codes:
                        composite = char + next_char
                        if composite in macron_map:
                            # Replace with mapped character and keep the combining character
                            mapped_char = macron_map[composite]
                            new_line.append(mapped_char + next_char)
                            i += 2  # Skip the next character as it has been processed
                            continue
                new_line.append(char)
                i += 1

            # Write the processed characters back into a string and write to output
            outfile.write(''.join(new_line))

    print(f"Processed file written to {output_file_path}")

# Example usage
input_file_path = 'crawl_wiktionary/macrons_wiktionary_test.txt'
output_file_path = 'crawl_wiktionary/macrons_wiktionary_test_format.txt'
macron_map = {
    '\u03B1\u0306': 'α',  
    '\u0391\u0306': 'Α',  
    '\u03B1\u0304': 'α',  
    '\u0391\u0304': 'Α',  
    '\u03B9\u0306': 'ι',  
    '\u0399\u0306': 'Ι',  
    '\u03B9\u0304': 'ι',  
    '\u0399\u0304': 'Ι',  
    '\u03C5\u0306': 'υ',  
    '\u03A5\u0306': 'Υ',  
    '\u03C5\u0304': 'υ',  
    '\u03A5\u0304': 'Υ',  
}
replace_composites(input_file_path, output_file_path, macron_map)