import unicodedata
import re
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pyuca import Collator
from utils import Colors, all_vowels, all_consonants


# Define a compiled regex for vowels and consonants for efficiency
vowels_pattern = re.compile(all_vowels)
consonants_pattern = re.compile(all_consonants)

def is_composite(char):
    """
    Determines if a character is a composite character, including those with
    components that match vowel or consonant regexes, but excluding characters
    that wholly map to single characters in the regexes.
    """
    decomposed = unicodedata.decomposition(char)
    if decomposed:
        # Split the decomposed form into its component parts
        parts = decomposed.split()
        # For each part, get the character and check against the regexes
        for part in parts:
            # Convert part back to character to check against regexes
            part_char = chr(int(part, 16))
            # If any part does not match vowels or consonants patterns, it's considered composite
            if not vowels_pattern.match(part_char) and not consonants_pattern.match(part_char):
                return True
        # If all parts match vowels or consonants, it's not considered uniquely composite
        return False
    else:
        # Character is not composite
        return False


def unicode_info(char):
    code = f"U+{ord(char):04X}"
    try:
        name = unicodedata.name(char)
    except ValueError:
        name = "UNKNOWN"
    return name, code

def find_unique_composites(input_file_path, output_file_path):
    unique_composites = {}

    with open(input_file_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            for char in line.strip():
                if is_composite(char):
                    decomposed = unicodedata.decomposition(char).split()
                    if len(decomposed) > 1:  # Ensure we're dealing with actual composites
                        key = "+".join(decomposed)
                        if key not in unique_composites:
                            name, code = unicode_info(char)
                            unique_composites[char] = f"{char} ({name})"

    # Sort the dictionary by the composite characters using pyuca Collator
    collator = Collator()
    sorted_composites = sorted(unique_composites.items(), key=lambda item: collator.sort_key(item[0]))

    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        outfile.write("format_dictionary = {\n")
        for char, info in sorted_composites:
            decomposed = "+".join(unicodedata.decomposition(char).split())
            outfile.write(f"    '\\u{decomposed.replace('+', '\\u')}': '',  # {info}\n")
        outfile.write("}\n")

    return unique_composites


# Example usage
input_file_path = 'crawl_wiktionary/macrons_wiktionary_raw.txt'
output_file_path = 'crawl_wiktionary/format_dictionary.py'
#find_unique_composites(input_file_path, output_file_path)


def find_unique_characters(input_file_path):
    unique_characters = set()
    collator = Collator()

    with open(input_file_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            for char in line.strip():
                if not re.match(vowels_pattern, char) and not re.match(consonants_pattern, char):
                    unique_characters.add(char)

    sorted_characters = sorted(unique_characters, key=collator.sort_key)
    return ''.join(sorted_characters)

# Replace 'input_file_path' with the actual path of your input text file
#input_file_path = 'crawl_wiktionary/macrons_wiktionary_raw.txt'
#unique_characters = find_unique_characters(input_file_path)
#print(unique_characters)

######

# List of specific characters to search for in the compositions
specific_chars = {'ᾰ', 'Ᾰ', 'ᾱ', 'Ᾱ', 'ῐ', 'Ῐ', 'ῑ', 'Ῑ', 'ῠ', 'Ῠ', 'ῡ', 'Ῡ'}

def find_composites_with_specific_diacritics(input_file_path, output_file_path):
    # Define the unicode points for combining breve and macron
    diacritics = {'0306', '0304'}
    unique_composites = set()

    with open(input_file_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            for char in line.strip():
                decomposition = unicodedata.decomposition(char).split()
                print(decomposition, char)
                if any(part in diacritics for part in decomposition):
                    unique_composites.add(char)

    # Sort the characters using pyuca Collator
    collator = Collator()
    sorted_composites = sorted(unique_composites, key=collator.sort_key)

    # Join the sorted characters into a single string
    sorted_composites_str = ''.join(sorted_composites)

    # Write the sorted characters to the output file
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        outfile.write(sorted_composites_str)

    print(sorted_composites_str)

    return sorted_composites_str

input_file_path = 'crawl_wiktionary/macrons_wiktionary_test.txt'
output_file_path = 'crawl_wiktionary/macrons_wiktionary_test_format.txt'
find_composites_with_specific_diacritics(input_file_path, output_file_path)

############################PLAYGROUND######################################

def remove_duplicates(s):
    seen = set()
    result = []
    for char in s:
        if char not in seen:
            seen.add(char)
            result.append(char)
    return ''.join(result)

all_unique_vowels = remove_duplicates(all_vowels.upper())


def sort_polytonic_string(input_string):
    c = Collator()

    # Split the string into a list of characters
    characters = list(input_string)

    # Sort the characters based on their collation order
    sorted_characters = sorted(characters, key=lambda char: c.sort_key(char))

    # Join the sorted characters back into a string
    sorted_string = ''.join(sorted_characters)

    return sorted_string

#print(all_unique_vowels)
#print(sort_polytonic_string(all_unique_vowels)[7:])

# ΆΈΉΊΌΎΏΪ́ΥἌἍἜἝἬἭἼἽὌὍ̓ὝὬὭᾺῈῊῚῸῪῺ̀ἊἋἚἛἪἫἺἻὊὋὛὪὫΑ͂ΗΩἏἎἮἯἾἿὟὮὯΕΟἈἉἘἙἨἩἸἹὈὉὙὨὩΪΫ
# ΑἈἌἊἎἉἍἋἏΆᾺΕἘἜἚἙἝἛΈῈΗἨἬἪἮἩἭἫἯΉῊΙἸἼἺἾἹἽἻἿΊῚΪΟὈὌὊὉὍὋΌῸΥὙὝὛὟΎῪΫΩὨὬὪὮὩὭὫὯΏῺ 71?

#print(sort_polytonic_string('άέήίόύώΐΰἄἅἔἕἤἥἴἵὄὅὔὕὤὥᾄᾅᾴᾔᾕῄᾤᾥῴ'))


# Example usage
#char = 'ᾰ̓'
#details = unicode_names_and_codes(char)
#print(details)