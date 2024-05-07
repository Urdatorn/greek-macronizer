'''
ALGORITHMIC MACRONIZING PART 2

Leverage morphological analysis to separate stems and endings for macronisation

Position in general algorithmic process: 
    (i) macronize all accentually-determined "free" macrons that were not filtered out by filter_dichrona.py because the token also contained one or more "true dichrona"
==> (ii) generalize the already macronized tokens by rule-bound inferences
    (iii) generalize whatever endings are left over algorithmically

RULES

Prefixes
Endings

'''

import re
import csv
import os
import sys
import unicodedata

from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import Colors, DICHRONA, only_bases, all_vowels
from erics_syllabifier import patterns
from prepare_tokens.filter_dichrona import ultima, properispomenon, proparoxytone
from collate_macrons import collate_macrons


from greek_inflexion_interface import get_stem


print(get_stem('φέρω', 'v1spia---'))
print(get_stem('λέγεις', 'v2spia---'))

def process_stem(token, tag):
    result = get_stem(token, tag)
    return result is not None

def count_found_stems(filepath):
    # Load all data first to avoid concurrency issues with file reading
    data = []
    with open(filepath, newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip the header
        for row in reader:
            if len(row) >= 2:
                data.append((row[0], row[1]))
    
    # Process data in parallel
    count = 0
    with ThreadPoolExecutor() as executor:
        # Map data to the executor
        future_to_row = {executor.submit(process_stem, token, tag): (token, tag) for token, tag in data}
        
        # Generate a progress bar for completed tasks
        for future in tqdm(as_completed(future_to_row), total=len(data), desc="Processing stems"):
            if future.result():
                count += 1

    return count

print(count_found_stems('macrons_alg1_ultima.tsv'))

#if __name__ == '__main__':
#    input_tsv = 'macrons_wiki_hypo_ifth_lsj.tsv'
#    output_tsv = 'macrons_alg1_ultima.tsv'