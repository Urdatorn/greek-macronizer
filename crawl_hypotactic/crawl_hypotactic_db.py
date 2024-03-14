'''
Disambiguates dichrona in open syllables without diphthongs 
by searching for appearances in the manually scanned metrical corpus from Hypotactic

'''
# IMPORTS


# Append the root folder to sys.path to be able to import from /utils.py and /erics_syllabifier.py
# Assuming your script is in a subfolder one level deep from the root
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
import re
from tqdm import tqdm 
import sqlite3

from erics_syllabifier import patterns, syllabifier
from utils import Colors, DICHRONA, all_vowels # /utils.py


### AUXILIARY DEFINITIONS ###


def open_syllable(syllable):
    '''
    >>open_syllable('ἀγάπη')
    >>True
    '''
    if re.search(f'{all_vowels}$', syllable):
        return True
    else:
        return False


def open_syllable_with_dichrona(syllable):
    '''
    >>open_syllable_with_dichrona('ἀρχ')
    >>False
    >>open_syllable_with_dichrona('μεν')
    >>False
    >>open_syllable_with_dichrona('δα')
    >>True
    '''
    contains_dichrona = any(char in DICHRONA for char in syllable)
    
    if contains_dichrona and open_syllable(syllable):
        return True
    return False


def is_diphthong(chars):
    ''' Expects two characters '''
    # Check if the input matches either of the diphthong patterns
    for pattern in ['diphth_y', 'diphth_i']:
        if re.match(patterns[pattern], chars):
            return True
    return False


def has_iota_adscriptum(chars):
    ''' Expects two characters '''
    adscr_i_pattern = re.compile(patterns['adscr_i'])
    # Check if the two-character string matches the adscript iota pattern
    if adscr_i_pattern.match(chars):
        return True
    return False


def syllable_with_real_dichrona(syllable):
    """
    Determines if a given syllable string contains at least one character from the DICHRONA set 
    that does not form a diphthong with its neighboring character and does not have an iota adscriptum.

    This function iterates through each character in the input string and returns if three checks go through:
    1
    2. If the character, along with its preceding or succeeding character, forms a diphthong.
    3. If the character, along with its preceding or succeeding character, has an iota adscriptum.

    >>syllable_with_real_dichrona('χείρ')
    >>False
    """
    for i, char in enumerate(syllable):
        if char in DICHRONA:

            # Form pairs to check for diphthongs and adscriptum
            prev_pair = syllable[i-1:i+1] if i > 0 else ''
            next_pair = syllable[i:i+2] if i < len(syllable) - 1 else ''

            # Check if the character is part of a diphthong or has adscriptum
            if (prev_pair and (is_diphthong(prev_pair) or has_iota_adscriptum(prev_pair))) or \
               (next_pair and (is_diphthong(next_pair) or has_iota_adscriptum(next_pair))):
                continue  # Skip if any of these conditions are true

            # If the character passes all checks, the string contains a necessary DICHRONA character
            return True

    # If the loop completes without returning True, no necessary DICHRONA character was found
    return False


def open_syllable_with_real_dichrona(syllable):
    '''
    Finds the syllables that can be disambiguated metrically
    >>open_syllable_with_real_dichrona('ῥα')
    >>True
    >>open_syllable_with_real_dichrona('ῥαι')
    >>False
    >>open_syllable_with_real_dichrona('ἀρχ')
    >>False
    >>open_syllable_with_real_dichrona('χείρ')
    >>True
    '''
    if open_syllable(syllable) and syllable_with_real_dichrona(syllable):
        return True
    else:
        return False





###

def collate_metrical_information(db_path, token):
    """
    Fetches and analyzes metrical patterns for a given token from the SQLite database.
    Each metrical pattern is on the form 'ὄ^,πι_,σθεν^'.
    """
    # Connect to the database and fetch metrical patterns for the token
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT metrical_pattern FROM metrical_patterns WHERE token = ?", (token,))
        rows = cursor.fetchall()

    # Parse the fetched metrical patterns
    all_matches = []
    for row in rows:
        # Split each metrical pattern string into a list of syllables and indicators
        metrical_pattern = row[0].split(',')
        syllables_with_indicators = [syll[-1] for syll in metrical_pattern]  # Extracting metrical indicators
        all_matches.append(syllables_with_indicators)

    # Immediate return if all_matches is empty
    if not all_matches:
        return None

    # Verify that all metrical patterns are identical
    if not all(pattern == all_matches[0] for pattern in all_matches):
        return None

    # If all metrical patterns are consistent, prepare to annotate DICHRONA positions
    annotated_positions = []
    full_word = ''.join(syll[:-1] for syll in row[0].split(','))  # Reconstruct the full word without indicators
    current_position = 1

    for syll in row[0].split(','):
        syllable, indicator = syll[:-1], syll[-1]  # Split syllable from its indicator
        for char in syllable:
            if char in DICHRONA:
                annotation = f'{indicator}{current_position}'
                annotated_positions.append(annotation)
            current_position += 1

    return annotated_positions

#print(collate_metrical_information('crawl_hypotactic/metrical_patterns.db', 'ἀρχόμενος'))
#print(collate_metrical_information('crawl_hypotactic/metrical_patterns.db', 'Πολυξείνης'))

### MAIN FUNCTION ###


def create_output_database(db_path):
    """
    Creates the output database for storing tokens with annotated positions.
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS annotated_tokens (
            id INTEGER PRIMARY KEY,
            token TEXT NOT NULL,
            annotated_positions TEXT
        )
        ''')
        conn.commit()


# Configure logging
logging.basicConfig(filename='crawl_hypotactic/crawl_hypotactic.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def macronize_tokens(input_db_path, output_db_path, input_tsv_path):
    """
    Processes tokens to filter those that can be disambiguated metrically, queries for their metrical patterns,
    and stores the results in the output database.
    """
    total_tokens = 0
    macronized_tokens = 0

    # Count the total number of lines for tqdm's total argument
    with open(input_tsv_path, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)
    
    # Ensure the output database is set up
    create_output_database(output_db_path)
    
    with sqlite3.connect(input_db_path) as input_conn, sqlite3.connect(output_db_path) as output_conn:
        input_cursor = input_conn.cursor()
        output_cursor = output_conn.cursor()

        with open(input_tsv_path, 'r', encoding='utf-8') as infile:
            for line in tqdm(infile, total=total_lines, desc="Processing tokens"):
                total_tokens += 1
                token = line.strip().split('\t')[0]
                list_of_syllables = syllabifier(token)

                # Check if any syllable in the token meets the criteria
                if any(open_syllable_with_real_dichrona(syllable) for syllable in list_of_syllables):
                    annotated_positions = collate_metrical_information(input_db_path, token)
                    if annotated_positions:
                        # Insert the token and its annotated positions into the output database
                        output_cursor.execute('INSERT INTO annotated_tokens (token, annotated_positions) VALUES (?, ?)', (token, ','.join(annotated_positions)))
                        output_conn.commit()
                        macronized_tokens += 1
                    else:
                        logging.info(f"No metrical information found for token: {token}")
                    
    # Calculate and print the metrics
    percentage = (macronized_tokens / total_tokens) * 100 if total_tokens > 0 else 0
    logging.info(f"{Colors.RED}Tokens metrically macronized: {macronized_tokens}, which is {percentage:.2f}% of total tokens{Colors.ENDC}")
    print(f"{Colors.RED}Tokens metrically macronized: {macronized_tokens}, which is {percentage:.2f}% of total tokens{Colors.ENDC}")

# Example usage
input_db_path = 'crawl_hypotactic/metrical_patterns.db'
output_db_path = 'crawl_hypotactic/macrons_hypotactic.db'
input_tsv_path = 'prepare_tokens/tokens/tokens.txt'
macronize_tokens(input_db_path, output_db_path, input_tsv_path)