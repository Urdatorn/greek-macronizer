# NB: I believe the crawl of LSJ was subpar and above all not based
# on the latest, bigger tokens.tsv. So there may be more to add than 181 tokens. 
# Then again, it may be due to significant overlap between LSJ and ifthimos-hypotactic-wiki.

# NB2: This is the newest and most up-to-date of the collation scripts
#
'''
Collates two tsv files with ≥4 columns, in this precise way:
if the first columns (tokens) are equal, then the fourth column (macron) of base_tsv_path
is carefully integrated among the existing macrons and the source (here 'lsj') is written in the fifth coumn.
Only macrons for syllables that have no macron are written; there is no overwriting.
This same script can be adapted mutatis mutandis for all of my tsv-macron-collation needs.

My unit testing (April 19th) was the base tsv

ὠφελία	v1sria---	ὠφελία	^5	wiktionary
ὠφέλιμον	a-s---ma-	ὠφέλιμος	^5	wiktionary
ὤχμασεν	v3saia---	ὤχμασεν		

to which was added the tsv

ὠφελία	v1sria---	ὠφελία	^5_6	
ὠφέλιμον	a-s---ma-	ὠφέλιμος		
ὤχμασεν	v3saia---	ὤχμασεν	^3	

yielding the collated

ὠφελία	v1sria---	ὠφελία	^5_6	hypotactic
ὠφέλιμον	a-s---ma-	ὠφέλιμος	^5	wiktionary
ὤχμασεν	v3saia---	ὤχμασεν	^3	hypotactic

'''


import csv
import logging
import re
import unicodedata

from tqdm import tqdm

from utils import Colors

# Setup logging configuration
logging.basicConfig(filename='collate.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# AUXILIARIES RE OVERWRITING
# ordinal_in_existing
# insert_macron_in_order


def ordinal_in_existing(existing_macrons, new_macron):
    """
    Check if the ordinal of the new macron exists in the existing macrons string.
    `existing_macrons` is expected to be a string like '^1_2_13' representing positions with macrons.
    This function was well unit tested on April 18th.
    >>> ordinal_in_existing('^1_2_13', '^13')
    >>> True
    """
    if existing_macrons and new_macron:
        # Use regular expression to split the string at both '^' and '_'
        existing_ordinals = [int(''.join(filter(str.isdigit, macron))) for macron in re.split(r'[\^_]', existing_macrons) if macron.isdigit()]
        
        # Extract the numeric part from the new_macron and convert to int
        new_digits = ''.join(filter(str.isdigit, new_macron))
        if new_digits:  # Ensure that new_macron contains digits
            new_ordinal = int(new_digits)
            return new_ordinal in existing_ordinals
    return False


def insert_macron_in_order(existing_macrons, new_macron):
    """
    Insert a new macron, e.g. '^2', into an existing macrons string, e.g. '_1^3', in the correct ordinal position.
    Ensures that the integers in the resulting macrons are ordered arithmetically.
    Unit tested on April 18th.
    >>> insert_macron_in_order('_1^3^7', '^2')
    >>> '_1^2^3^7'
    >>> insert_macron_in_order('_1', '')
    >>> _1
    >>> insert_macron_in_order('', '^5')
    >>> ^5
    """
    if not existing_macrons:
        return new_macron
    
    if not new_macron or not new_macron[1:].isdigit():  # Check if new_macron is properly formatted
        return existing_macrons

    new_symbol, new_number = new_macron[0], int(new_macron[1:])

    if ordinal_in_existing(existing_macrons, new_macron):
        return existing_macrons  # If the new macron's ordinal is already present, return as is

    # Extract parts and their types (prefixes) while keeping them paired
    parts = re.findall(r'([\^_]\d+)', existing_macrons)
    parts = [(part[0], int(part[1:])) for part in parts]  # Split into (symbol, number)

    # Insert new macron in the correct position based on its ordinal
    inserted = False
    for i, (symbol, number) in enumerate(parts):
        if new_number < number:
            parts.insert(i, (new_symbol, new_number))
            inserted = True
            break
    if not inserted:
        parts.append((new_symbol, new_number))

    # Reconstruct the macrons string from sorted parts
    parts.sort(key=lambda x: x[1])  # Sort by number
    result = ''.join(f'{symbol}{number}' for symbol, number in parts)
    return result


def collate_macrons(existing_macrons, new_macrons):
    """
    Collates new macrons into existing macrons, handling complex macron inputs.
    See unit-test function below for the many cases this function can handle
    """
    if not existing_macrons:
        return new_macrons  # Return new macrons directly if no existing macrons

    if not new_macrons:
        return existing_macrons  # Return existing if no new macrons to add

    # Handle case where new_macrons contains multiple macron parts
    new_macron_parts = re.findall(r'[\^_]\d+', new_macrons)
    result_macrons = existing_macrons

    if len(new_macron_parts) == 1:
        # If only one macron part in new_macrons, process it directly
        return insert_macron_in_order(existing_macrons, new_macrons)
    else:
        # Iterate over each macron part in new_macrons and collate it into existing_macrons
        for macron in new_macron_parts:
            if not ordinal_in_existing(result_macrons, macron):
                result_macrons = insert_macron_in_order(result_macrons, macron)
        return result_macrons

def test_collate_macrons():
    tests = [
        # Test cases: (existing_macrons, new_macrons, expected_result)
        ("", "^2", "^2", "Empty existing macrons"),
        ("^1_3^7", "", "^1_3^7", "Empty new macrons"),
        ("^1_3^7", "^2", "^1^2_3^7", "Single new macron addition"),
        ("_1^3^7", "^2_5", "_1^2^3_5^7", "Multiple new macrons addition"),
        ("^1_3^7", "^3", "^1_3^7", "Redundant macron addition"),
        ("^1_3^7", "^5^2", "^1^2_3^5^7", "Unordered multiple new macrons"),
        ("_1^3^7", "_4^2", "_1^2^3_4^7", "Complex case with all types"),
        ("", "^1^2^3", "^1^2^3", "All new macrons, none existing")
    ]
    
    for existing, new, expected, description in tests:
        result = collate_macrons(existing, new)
        if result == expected:
            print(f"{Colors.GREEN}Success{Colors.ENDC}: {description} -> Expected: {expected}, Got: {result}")
        else:
            print(f"Failure: {description} -> Expected: {expected}, Got: {result}")


### COLLATION 


def collate_two_tsv(base_tsv_path, added_tsv_path, output_tsv_path):
    # Load the entries from added_tsv into a dictionary for fast lookup
    added_entries = {}
    with open(added_tsv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if row:  # Ensure the row is not empty
                key = unicodedata.normalize('NFC', row[0].strip()) # normalize the token to canonical composition
                added_entries[key] = row[3].strip() # the macrons are in the fourth column (i.e. 3 when zero counting)
    #print(added_entries)

    matching_lines = 0
    unmatched_lines = 0

    # Process base_tsv and append data from added_tsv where appropriate
    with open(base_tsv_path, 'r', encoding='utf-8') as base_file, \
         open(output_tsv_path, 'w', newline='', encoding='utf-8') as output_file:
        reader = csv.reader(base_file, delimiter='\t')
        writer = csv.writer(output_file, delimiter='\t')

        for base_row in tqdm(reader, desc="Collating entries"):
            if base_row and len(base_row) >= 4:
                token_in, tag_in, lemma_in, macron_in = base_row[:4]
                source_in = base_row[4] if len(base_row) > 4 else ''

                token = unicodedata.normalize('NFC', token_in.strip())
                #print(token)
                if token in added_entries:
                    new_macrons = added_entries[token]
                    updated_macron = collate_macrons(macron_in, new_macrons)
                    if updated_macron != macron_in:
                        matching_lines += 1
                        source_out = "lsj"
                    else:
                        source_out = source_in
                    macron_out = updated_macron
                    #print(f'Macron out is updated macron: {macron_out}')
                else:
                    macron_out = macron_in
                    #print(f'Macron out is old macron: {macron_in}')
                    source_out = source_in
                    unmatched_lines += 1

                # Write the modified row to the output file
                output_row = [token_in, tag_in, lemma_in, macron_out, source_out]
                writer.writerow(output_row)


    # Log the results
    logging.info(f"{Colors.GREEN}* Ifthimos * Total matching lines: {matching_lines}{Colors.ENDC}")
    logging.info(f"{Colors.RED}* Ifthimos * Total unmatched lines: {unmatched_lines}{Colors.ENDC}")
    print(f"{Colors.GREEN}* Ifthimos * Total matching lines: {matching_lines}{Colors.ENDC}")
    print(f"{Colors.RED}* Ifthimos * Total unmatched lines: {unmatched_lines}{Colors.ENDC}")


### USAGE

# Total matching lines: 181 (30 april)
collate_two_tsv('macrons_wiki_hypo_ifth.tsv', 'macrons_lsj.tsv', 'macrons_wiki_hypo_ifth_lsj.tsv')


### TEST
#collate_two_tsv('macrons_test2.tsv', 'macrons_test2_added.tsv', 'macrons_test2_result.tsv')
