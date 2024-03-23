import csv
import re
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tqdm import tqdm
from greek_accentuation.characters import strip_accents
from greek_accentuation.accentuation import make_oxytone

from erics_syllabifier import syllabifier
from utils import graves, Colors


#example = 'φάρμακος'
#no_accents = strip_accents(example)
#print(make_oxytone(no_accents))


def barytone(word):
    '''
    Uses regex from ./utils.py
    >> barytone('βασιλεὺς')
    >> True
    '''
    list_of_syllables = syllabifier(word)
    if len(list_of_syllables) >= 1: 
        ultima = list_of_syllables[-1]
        if re.search(graves, ultima):
            return True
        else:
            return False
    else:
        return False
    

def oxytone_from_barytone(word):
    '''
    >> oxytone_from_barytone('εὐδρακὴς')
    >> εὐδρακής
    '''
    if word and barytone(word):
        stripped = strip_accents(word)
        oxytoned = make_oxytone(stripped)
        return oxytoned
    else:
        return word


def process_tokens_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as infile, \
         open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')
        new_lines_count = 0  # Initialize counter for new lines

        for row in tqdm(reader, desc="Processing tokens"):
            # Write the original row
            writer.writerow(row)
            
            # Check if the token is barytone
            if barytone(row[0]):
                modified_row = row.copy()
                modified_row[0] = oxytone_from_barytone(row[0])
                
                # If the lemma is identical to the token, modify it as well
                if len(row) >= 3 and row[2] == row[0]:
                    modified_row[2] = oxytone_from_barytone(row[2])
                
                # Write the modified row
                writer.writerow(modified_row)
                new_lines_count += 1  # Increment the new lines counter

    print(f"{Colors.GREEN}Process complete. Modified tokens written to {output_file_path}{Colors.ENDC}")
    print(f"{Colors.GREEN}Total new lines created: {new_lines_count}{Colors.ENDC}")

