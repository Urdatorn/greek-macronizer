'''
Removes the extra accent on the ultima from tokens which were followed by a clitic in the corpus
'''

# IMPORTS

# Append the root folder to sys.path to be able to import from /utils.py
# Assuming your script is in a subfolder one level deep from the root
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re # for the regex patterns
from greek_accentuation.characters import base

# local imports
from utils import Colors # /utils.py
from erics_syllabifier import syllabifier # /prepare_tokens/erics_syllabifier.py

# END OF IMPORTS

# all accented characters 
acutes = r'[άέήίόύώἄἅἔἕἤἥἴἵὄὅὔὕὤὥΐΰᾄᾅᾴᾔᾕῄᾤᾥῴ]'
graves = r'[ὰὲὴὶὸὺὼἂἃἒἓἢἣἲἳὂὃὒὓὢὣῒῢᾂᾃᾲᾒᾓῂᾢᾣῲ]'
circumflexes = r'[ᾶῆῖῦῶἇἆἦἧἶἷὖὗὦὧἦἧἆἇὧὦᾆᾇᾷᾖᾗᾦᾧῷῇ]'
all_accents = r'[άέήίόύώἄἅἔἕἤἥἴἵὄὅὔὕὤὥΐΰᾄᾅᾴᾔᾕῄᾤᾥῴὰὲὴὶὸὺὼἂἃἒἓἢἣἲἳὂὃὒὓὢὣῒῢᾂᾃᾲᾒᾓῂᾢᾣῲᾶῆῖῦῶἇἆἦἧἶἷὖὗὦὧἦἧἆἇὧὦᾆᾇᾷᾖᾗᾦᾧῷῇ]'

def remove_double_accents(word):
    list_of_syllables = syllabifier(word)  # Syllabify the word
    ultima = list_of_syllables[-1]  # Get the last syllable (ultima)
    
    # Count the number of accents in the ultima before any changes
    accents_before = len(re.findall(all_accents, ultima))
    
    # Check if the word contains two or more accents in total
    if len(re.findall(all_accents, word)) > 1:
        # If so, and if the ultima contains an accent, we process it
        if re.search(all_accents, ultima):
            # Remove the accent from the ultima by replacing each accented character with its base character
            ultima_cleaned = ''.join(base(char) for char in ultima)

            # Replace the old ultima with the cleaned one in the list of syllables
            list_of_syllables[-1] = ultima_cleaned

            # Reconstruct the word from the list of syllables
            word_cleaned = ''.join(list_of_syllables)
            
            # Count the number of accents in the cleaned ultima
            accents_after = len(re.findall(all_accents, ultima_cleaned))
            
            # Calculate the number of accents removed from the ultima
            accents_removed = accents_before - accents_after
            
            return word_cleaned, accents_removed
    # If the word doesn't meet the criteria for processing, return it unchanged along with 0 to indicate no accents were removed
    return word, 0

def process_file(input_file_path, output_file_path):
    total_accents_removed = 0
    with open(input_file_path, 'r', encoding='utf-8') as infile, \
         open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            columns = line.strip().split('\t')
            if columns:
                modified_word, accents_removed = remove_double_accents(columns[0])
                total_accents_removed += accents_removed
                columns[0] = modified_word
                modified_line = '\t'.join(columns) + '\n'
                outfile.write(modified_line)
                
    print(f"{Colors.RED}Total accents removed: {total_accents_removed}{Colors.ENDC}")


# print(remove_double_accents('οἷόν'))




