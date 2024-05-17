'''
Some tools to generate the stats needed for keeping track of progress (through the web interface)
'''

import csv
import re

from erics_syllabifier import syllabifier
from utils import open_syllable, DICHRONA, only_bases


def non_hidden_quantity(word):
    '''
    >>> non_hidden_quantity('δυστυχές')
    >>> ['τυ']
    '''
    non_hidden_quantities = []
    syllables = syllabifier(word)
    if syllables:
        for syllable in syllables:
            if open_syllable(syllable) and any(char in DICHRONA for char in syllable):
                non_hidden_quantities.append(syllable)
    return non_hidden_quantities


def total_non_hidden_quantities_in_tsv(input_tsv):
    total_sum = 0
    first_line = True  # Flag to identify the header

    with open(input_tsv, mode='r', encoding='utf-8', newline='') as infile:
        reader = csv.reader(infile, delimiter='\t')

        for row in reader:
            if first_line:
                # Skip the header line
                first_line = False
                continue

            if row:
                word = row[0]
                non_hidden_quantities = non_hidden_quantity(word)
                total_sum += len(non_hidden_quantities)

    return total_sum


def count_macrons_in_tsv(input_tsv):
    macron_pattern = re.compile(r'[\^_](\d{1,2})')  # Matches ^1 to ^99 or _1 to _99
    total_macrons = 0

    with open(input_tsv, mode='r', encoding='utf-8', newline='') as infile:
        reader = csv.reader(infile, delimiter='\t')
        first_line = True  # Flag to skip the header

        for row in reader:
            if first_line:
                first_line = False
                continue

            if row and len(row) >= 4:
                macron_column = row[3]
                macrons = macron_pattern.findall(macron_column)
                total_macrons += len(macrons)

    return total_macrons


def count_unhidden_macrons_in_tsv(input_tsv):
    macron_pattern = re.compile(r'[\^_](\d{1,2})')  # Matches ^1 to ^99 or _1 to _99
    total_macrons = 0
    first_line = True  # Flag to skip the header

    with open(input_tsv, mode='r', encoding='utf-8', newline='') as infile:
        reader = csv.reader(infile, delimiter='\t')

        for row in reader:
            if first_line:
                first_line = False
                continue

            if row and len(row) >= 4:
                word = row[0]
                macron_column = row[3]

                # Find all macrons in the macron column
                macrons = macron_pattern.findall(macron_column)
                
                # Apply the non_hidden_quantity function to get the constraint
                non_hidden_quantities = non_hidden_quantity(word)
                max_count = len(non_hidden_quantities)

                # Count the macrons up to the allowed limit
                total_macrons += min(len(macrons), max_count)

    return total_macrons


def count_unique_first_column(input_tsv):
    unique_values = set()

    with open(input_tsv, mode='r', encoding='utf-8', newline='') as infile:
        reader = csv.reader(infile, delimiter='\t')
        first_line = True  # Flag to skip the header

        for row in reader:
            if first_line:
                first_line = False
                continue

            if row:
                first_column_value = row[0]
                unique_values.add(first_column_value)

    return len(unique_values)


input_tsv = 'macrons_alg3_prefix.tsv'
print(f'Non-hidden dichrona: {total_non_hidden_quantities_in_tsv(input_tsv)}')
print(f'Macrons capped by non-hidden: {count_unhidden_macrons_in_tsv(input_tsv)}')
print(f'Macrons: {count_macrons_in_tsv(input_tsv)}')
print(f"Number of unique first column values: {count_unique_first_column(input_tsv)}")
