'''
Disambiguates dichrona in open syllables without diphthongs 
by searching for appearances in the manually scanned metrical corpus from Hypotactic

DIPHTHONGS GO THROUGH
e.g. it marks the ypsilon in ἀβουλιᾶν as long :(

the problem is the any in 
    if any(open_syllable_with_real_dichrona(syllable) for syllable in list_of_syllables)

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
    metrical_patterns.db entries look like this:
    token   metrical_pattern
        ὦ	    ὦ_
        παῖ,	παῖ,_
        τέλος	τέ^,λος_
    Returned annotated_positions is a list of length + position like ['^1', '_4']
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


def get_syllable_spans(list_of_syllables):
    """
    Returns a list of tuples, each representing the start and end character positions of a syllable
    and its index within the list_of_syllables, to help map characters to their syllable.
    >>get_syllable_spans(syllabifier('πατρός'))
    >>[(1, 3, 0), (4, 6, 1)]
    """
    syllable_spans = []
    position = 1

    for i, syllable in enumerate(list_of_syllables):
        start_position = position
        end_position = start_position + len(syllable) - 1
        syllable_spans.append((start_position, end_position, i))
        position += len(syllable)

    return syllable_spans


def filter_syllables(annotated_positions, token):
    """
    Filters the annotated positions returned by collate_metrical_information based on whether
    the corresponding syllables pass the open_syllable_with_real_dichrona check.
    """
    # Use syllabifier to get the 'master' syllabification of the token
    list_of_syllables = syllabifier(token)
    syllable_spans = get_syllable_spans(list_of_syllables)

    # Initialize a list to hold the filtered annotations
    filtered_annotations = []

    # Iterate through annotated_positions to filter based on open_syllable_with_real_dichrona
    for annotation in annotated_positions:
        indicator = annotation[0]  # '^' or '_'
        position = int(annotation[1:])  # Extract the position number from annotation

        # Check which syllable this position falls into
        for start, end, index in syllable_spans:
            if start <= position <= end:
                # Check if the syllable passes the open_syllable_with_real_dichrona check
                if open_syllable_with_real_dichrona(list_of_syllables[index]):
                    # Include this annotation
                    filtered_annotations.append(annotation)
                break  # No need to check further spans

    return filtered_annotations


### MAIN FUNCTION ###


def create_output_database(db_path):
    """
    Creates the output database for storing tokens along with tag, lemma, and macrons.
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS annotated_tokens (
            id INTEGER PRIMARY KEY,
            token TEXT NOT NULL,
            tag TEXT,
            lemma TEXT,
            macrons TEXT
        )
        ''')
        conn.commit()


# Configure logging
logging.basicConfig(filename='crawl_hypotactic/crawl_hypotactic.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def macronize_tokens(input_db_path, output_db_path, input_tsv_path):
    """
    Processes tokens to filter those that can be disambiguated metrically, queries for their metrical patterns,
    and stores the results in the output database, including token, tag, lemma, and macrons.
    """
    total_tokens = 0
    macronized_tokens = 0

    # Ensure the output database is set up
    create_output_database(output_db_path)
    
    with sqlite3.connect(input_db_path) as input_conn, sqlite3.connect(output_db_path) as output_conn:
        input_cursor = input_conn.cursor()
        output_cursor = output_conn.cursor()

        with open(input_tsv_path, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        # Wrap the line processing with tqdm for progress indication
        for line in tqdm(lines, desc="Processing tokens", total=len(lines)):
            parts = line.strip().split('\t')
            if len(parts) >= 3:  # Ensure there are enough parts
                total_tokens += 1
                token, tag, lemma = parts[0], parts[1], parts[2]
                list_of_syllables = syllabifier(token)

                # Check if any syllable in the token meets the criteria for filtering
                if any(open_syllable_with_real_dichrona(syllable) for syllable in list_of_syllables):
                    # Fetch consistent metrical annotations for the token
                    consistent_metrical_annotations = collate_metrical_information(input_db_path, token)
                    
                    # Proceed to filter these annotations based on syllable criteria
                    if consistent_metrical_annotations:
                        filtered_annotations = filter_syllables(consistent_metrical_annotations, token)
                        if filtered_annotations:
                            # Insert the token, tag, lemma, and filtered macrons into the output database
                            output_cursor.execute('INSERT INTO annotated_tokens (token, tag, lemma, macrons) VALUES (?, ?, ?, ?)', 
                                                  (token, tag, lemma, ','.join(filtered_annotations)))
                            output_conn.commit()
                            macronized_tokens += 1
                        else:
                            logging.info(f"Filtered all metrical information for token: {token}")
                    else:
                        logging.info(f"No consistent metrical information found for token: {token}")
                else:
                    logging.info(f"No syllable meets criteria for token: {token}")
                    
    # Calculate and print the metrics
    percentage = (macronized_tokens / total_tokens) * 100 if total_tokens > 0 else 0
    logging.info(f"{Colors.RED}Tokens metrically macronized: {macronized_tokens}, which is {percentage:.2f}% of total tokens{Colors.ENDC}")
    print(f"{Colors.RED}Tokens metrically macronized: {macronized_tokens}, which is {percentage:.2f}% of total tokens{Colors.ENDC}")


# Example usage
input_db_path = 'crawl_hypotactic/metrical_patterns.db'
output_db_path = 'crawl_hypotactic/macrons_hypotactic.db'
input_tsv_path = 'prepare_tokens/tokens/tokens.txt'
macronize_tokens(input_db_path, output_db_path, input_tsv_path)