'''
Disambiguates dichrona in open syllables by searching for appearances in the manually scanned metrical corpus from Hypotactic
'''
# IMPORTS


# Append the root folder to sys.path to be able to import from /utils.py and /erics_syllabifier.py
# Assuming your script is in a subfolder one level deep from the root
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
import re
from bs4 import BeautifulSoup
from tqdm import tqdm  # Import tqdm for the progress bar

from erics_syllabifier import patterns, syllabifier
from utils import Colors, DICHRONA, all_vowels # /utils.py


### AUXILIARY DEFINITIONS ###


def find_syllable_lengths(html_content, input_word):
    soup = BeautifulSoup(html_content, 'html.parser')
    syllable_lengths = []
    
    for word_div in soup.find_all(class_="word"):
        syllables = [(syll.text, 'long' if 'long' in syll.get('class', []) else 'short') for syll in word_div.find_all('span')]
        reconstructed_word = ''.join(syll[0] for syll in syllables)
        
        if reconstructed_word == input_word:
            formatted_syllables = [[syll[0], '_' if syll[1] == 'long' else '^'] for syll in syllables]
            syllable_lengths.append(formatted_syllables)
    
    return syllable_lengths


def process_html_files_in_folder(input_word):
    '''
    Input: word, e.g. ἀρχόμενος
    Output: lists of syllable lengths from all appearances in the corpus, e.g. 
    [['ἀ', '_'], ['ρχό', '^'], ['με', '^'], ['νος', '_']]
    [['ἀρχ', '_'], ['όμ', '^'], ['εν', '^'], ['ος', '_']]
    '''
    folder_path = 'crawl_hypotactic/hypotactic_htmls_greek'
    all_matches = []
    html_files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
    
    # Wrap the file iteration with tqdm for a progress bar
    for filename in tqdm(html_files, desc="Processing files"):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        matches = find_syllable_lengths(html_content, input_word)
        if matches:
            all_matches.extend(matches)
    
    return all_matches


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


### MAIN FUNCTIONS ###


def collate_metrical_information(all_matches):
    '''
    Input:  lists of syllable lengths from all appearances in the corpus, e.g. 
            [['ἀ', '_'], ['ρχό', '^'], ['με', '^'], ['νος', '_']]
            [['ἀρχ', '_'], ['όμ', '^'], ['εν', '^'], ['ος', '_']]
    Output: None, if the metrical patterns disagree, 
            otherwise 
    '''
    # Immediate return if all_matches is empty
    if not all_matches:
        return None

    # Step 1: Check for consistent metrical patterns across all matches
    metrical_patterns = [['^' if syll_len == '^' else '_' for _, syll_len in match] for match in all_matches]
    
    # Verify that all metrical patterns are identical
    if not metrical_patterns or not all(pattern == metrical_patterns[0] for pattern in metrical_patterns):
        return None

    # Use the first match to reconstruct the full word and analyze it
    reference_match = all_matches[0]
    full_word = ''.join(syll for syll, _ in reference_match)
    metrical_pattern = metrical_patterns[0]

    # Prepare to annotate DICHRONA positions
    annotated_positions = []
    current_position = 1  # Initialize character position counter

    for syllable, length_indicator in reference_match:
        for char in syllable:
            # If the character is DICHRONA, annotate it based on its syllable length
            if char in DICHRONA:
                annotation = f'{length_indicator}{current_position}'
                annotated_positions.append(annotation)
            current_position += 1

    return annotated_positions


# Configure logging
logging.basicConfig(filename='crawl_hypotactic/crawl_hypotactic.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def macronize_tokens(input_tsv_path, output_tsv_path):
    total_tokens = 0
    macronized_tokens = 0
    
    with open(input_tsv_path, 'r', encoding='utf-8') as infile, \
         open(output_tsv_path, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            total_tokens += 1
            token = line.strip().split('\t')[0]
            
            # Gather all matches for the current token
            all_matches = process_html_files_in_folder(token)
            
            # Apply collate_metrical_information
            annotated_positions = collate_metrical_information(all_matches) if all_matches else None
            
            if annotated_positions:
                # Write the original token and the annotated positions to the output file
                outfile.write(f"{token}\t{','.join(annotated_positions)}\n")
                macronized_tokens += 1
            elif all_matches is not None and annotated_positions is None:
                # Log the case of inconsistent metrical patterns
                logging.info(f"Inconsistent metrical patterns for token: {token}")
            elif not all_matches:
                # Log the case where no matches are found
                logging.info(f"No matches found for token: {token}")
                    
    # Calculate and print the metrics
    percentage = (macronized_tokens / total_tokens) * 100 if total_tokens > 0 else 0
    logging.info(f"{Colors.RED}Tokens metrically macronized: {macronized_tokens}, which is {percentage:.2f}% of total tokens{Colors.ENDC}")

# Example usage
input_tsv_path = 'prepare_tokens/tokens/tokens.txt'
output_tsv_path = 'crawl_hypotactic/macrons_hypotactic.txt'
macronize_tokens(input_tsv_path, output_tsv_path)




# Example usage
#input_folder_path = 'crawl_hypotactic/hypotactic_htmls_greek'  # Update this path
#input_word = "ἀρχόμενος"
#matches = process_html_files_in_folder(input_folder_path, input_word)

#for match in matches:
#    print(match)

'''
Great. Now define a function disambiguate_dichrona_in_open_vowels(word), that given list_of_syllables = syllabifier(word), checks whether any entries in list_of_syllables are  open_syllable_with_dichrona. If it finds some, it applies process_html_files_in_folder(input_word) (I've hardcoded the file path, so it only takes one arg) to all of them. It returns a TSV line where the first column is the input word, and the second column is 
'''

'''
Now define a function collate_metrical_information(all_matches) that given all the lists output by process_html_files_in_folder(input_word) on the form [['ἀ', '_'], ['ρχό', '^'], ['με', '^'], ['νος', '_']], checks whether the ordered set of only the syllable lengths (here _, ^, ^. _) i.e. the second elements in the list of dyads, is the same in all of the output lists. If so, then for every DICHRONA in the syllable of a dyad with syllable length '_', return _n, where n is the ordinal number (starting from 1) of the character in the word consisting of all the syllables (i.e. ἀ would be _1 because it is character 1 in ἀρχόμενος), and for every DICHRONA  in the syllable of a dyad with syllable length '^', return ^n, where n is again the ordinal number starting from 1. Taken together, given a set of lists like 

[['ἀρ', '_'], ['χό', '^'], ['με', '^'], ['νος', '_']]
[['ἀρχ', '_'], ['όμ', '^'], ['εν', '^'], ['ος', '_']]
[['ἀρ', '_'], ['χό', '^'], ['με', '^'], ['νος', '_']]

the function would see that they all give the same ordered series of syllable lengths (notwithstanding the different syllables). It then outputs _1 because there is only one DICHRONA and it is the first character. For simplicity, the function that use the first of the lists as a reference point when joining the syllables and calculating the ordinals.
'''