import re
import sqlite3
import csv
import logging
from tqdm import tqdm
from utils import Colors, all_vowels, with_spiritus, only_bases


## PREP


def lacks_spiritus(word):
    """
    Checks if the first character of the word is a vowel and
    if the word does not contain any characters with spiritus.
    """
    if word:
        if re.match(all_vowels, word[0]) and not re.search(with_spiritus, word):
            return True  
    return False


def count_equivalent_entries(text_file_path, db_path, table_name, column_name):
    # Load the entries from the text file into a set for fast lookup
    with open(text_file_path, 'r', encoding='utf-8') as file:
        text_file_entries = set(line.split('\t')[0] for line in file)

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to select all entries from the specified column and table
    query = f"SELECT {column_name} FROM {table_name}"
    cursor.execute(query)
    
    # Fetch all database entries and store them in a set
    db_entries = set(row[0] for row in cursor.fetchall())

    # Close the database connection
    conn.close()

    # Calculate and return the number of equivalent entries
    equivalent_entries = text_file_entries.intersection(db_entries)
    return len(equivalent_entries)


def count_equivalent_entries_no_spiritus(text_file_path, db_path, table_name, column_name):
    # Load the entries from the text file into sets for fast lookup
    text_file_entries = set()
    text_file_entries_base = set()

    with open(text_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            entry = line.split('\t')[0]
            if lacks_spiritus(entry):
                text_file_entries_base.add(only_bases(entry))
            else:
                text_file_entries.add(entry)

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to select all entries from the specified column and table
    query = f"SELECT {column_name} FROM {table_name}"
    cursor.execute(query)
    
    # Fetch all database entries and store them in sets
    db_entries = set(row[0] for row in cursor.fetchall())
    db_entries_base = set(only_bases(entry) for entry in db_entries)

    # Close the database connection
    conn.close()

    # Calculate and return the number of equivalent entries
    equivalent_entries = len(text_file_entries.intersection(db_entries))
    equivalent_entries_base = len(text_file_entries_base.intersection(db_entries_base))
    
    return equivalent_entries + equivalent_entries_base


# Example usage:
#total_equivalent_entries_no_spiritus = count_equivalent_entries_no_spiritus('crawl_wiktionary/macrons_wiktionary_nfc.tsv', 'macrons.db', 'annotated_tokens', 'token')
#print(f'Total equivalent entries, comparing stripped bases for tokens lacking spiritus: {total_equivalent_entries_no_spiritus}')

#total_equivalent_entries = count_equivalent_entries('crawl_wiktionary/macrons_wiktionary_nfc.tsv', 'macrons.db', 'annotated_tokens', 'token')
#print(f'Total equivalent entries: {total_equivalent_entries}')


### AUXILIARY FUNCTIONS


# Initialize logging
logging.basicConfig(filename='macrons_collate_wiktionary.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_existing_macrons(cursor, token):
    """Fetch the existing macrons for a given token from the database."""
    cursor.execute("SELECT macrons FROM annotated_tokens WHERE token = ?", (token,))
    result = cursor.fetchone()
    return result[0] if result else None

import re


def ordinal_in_existing(existing_macrons, new_macron):
    """
    Check if the ordinal of the new macron exists in the existing macrons string.
    `existing_macrons` is expected to be a string like '^1_2_13' representing positions with macrons.
    Unit tested on April 18th.
    >>> ordinal_in_existing('^1_2_13', '^13')
    >>> True
    """
    if existing_macrons and new_macron:
        # Use regular expression to split the string at both '^' and '_'
        existing_ordinals = [int(''.join(filter(str.isdigit, macron))) for macron in re.split(r'[\^_]', existing_macrons) if macron.isdigit()]
        #print(f"Existing ordinals: {existing_ordinals}")
        
        # Extract the numeric part from the new_macron and convert to int
        new_ordinal = int(''.join(filter(str.isdigit, new_macron)))
        #print(f"New ordinal: {new_ordinal}")
        
        if new_ordinal in existing_ordinals:
            return True
    return False

# Example usage:
print(ordinal_in_existing('', '^13'))  # Expected: True, because 13 is explicitly listed
print(ordinal_in_existing('^1_2_13', ''))  # Expected: True, because 13 is explicitly listed
print(ordinal_in_existing('^1_2_13', '^13'))  # Expected: True, because 13 is explicitly listed


def insert_macron_in_order(existing_macrons, new_macron):
    if not existing_macrons:
        return new_macron  # Directly return the new macron if no existing macrons are present
    
    if not new_macron or ordinal_in_existing(existing_macrons, new_macron):
        return existing_macrons  # Return unchanged if the new macron's ordinal is already present

    # Parse the existing macrons into parts and sort them by their ordinal numbers
    parts = re.findall(r'([\^_]\d+)', existing_macrons)
    new_symbol, new_number = new_macron[0], int(new_macron[1:])

    # Insert in the correct position based on the ordinal number
    inserted = False
    for i, part in enumerate(parts):
        symbol, number = part[0], int(part[1:])
        if new_number < number:
            parts.insert(i, new_macron)
            inserted = True
            break
    if not inserted:
        parts.append(new_macron)

    # Sort the parts to ensure they are in ascending order and concatenate them back to a string
    parts.sort(key=lambda x: int(re.search(r'\d+', x).group()))
    return ''.join(parts)

# Test the functions with edge cases and typical use cases
print(insert_macron_in_order('_1^3^7', '^2'))  # Expected: '_1^2^3^7'
print(insert_macron_in_order('', '^5'))        # Expected: '^5'
print(insert_macron_in_order('_3^5', '_1'))    # Expected: '_1_3^5'

# Example usage:
print(insert_macron_in_order('_1', ''))  # Expected: '_1^2^3^7'
print(insert_macron_in_order('', '^5'))  # Output should be '^1_3^5^7'
print(insert_macron_in_order('^1_3^7', '^5'))  # Output should be '^1_3^5^7'
print(insert_macron_in_order('_1^3^7', '^8'))  # Output should be '_1^3^7^8'



def update_macrons(db_path, token, macrons, cursor):
    """Update the macrons for a given token in the database."""
    existing_macrons = fetch_existing_macrons(cursor, token)
    macrons_written = macrons_appended = skipped_already_present = skipped_no_token_match = 0

    if existing_macrons is None:
        skipped_no_token_match += 1
    elif existing_macrons == '':
        cursor.execute("UPDATE annotated_tokens SET macrons = ?, source = 'wiktionary' WHERE token = ?", (macrons, token))
        macrons_written += 1
    else:
        if not any(ordinal_in_existing(existing_macrons, m) for m in macrons.split(',')):
            updated_macrons = insert_macron_in_order(existing_macrons, macrons)
            cursor.execute("UPDATE annotated_tokens SET macrons = ?, source = 'wiktionary' WHERE token = ?", (updated_macrons, token))
            macrons_appended += 1
        else:
            skipped_already_present += 1
    
    return macrons_written, macrons_appended, skipped_already_present, skipped_no_token_match

def process_wiktionary_entries(db_path, wiktionary_path):
    """Process Wiktionary entries to update macrons in the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    macrons_written = macrons_appended = skipped_already_present = skipped_no_token_match = 0
    
    with open(wiktionary_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for line in tqdm(reader, desc="Processing Wiktionary entries"):
            if len(line) >= 2:
                token, macrons = line[0], line[1]
                written, appended, skipped_present, skipped_no_match = update_macrons(db_path, token, macrons, cursor)
                macrons_written += written
                macrons_appended += appended
                skipped_already_present += skipped_present
                skipped_no_token_match += skipped_no_match

    conn.commit()
    conn.close()

    # Log and print the summary
    logging.info(f"Macrons written: {macrons_written}")
    logging.info(f"Macrons appended: {macrons_appended}")
    logging.info(f"Skipped (macrons already present): {skipped_already_present}")
    logging.info(f"Skipped (no token match): {skipped_no_token_match}")
    print(f"{Colors.GREEN}Macrons written: {macrons_written}{Colors.ENDC}")
    print(f"{Colors.GREEN}Macrons appended: {macrons_appended}{Colors.ENDC}")
    print(f"{Colors.RED}Skipped (macrons already present): {skipped_already_present}{Colors.ENDC}")
    print(f"{Colors.RED}Skipped (no token match): {skipped_no_token_match}{Colors.ENDC}")


# Example usage
db_path = "macrons.db"
wiktionary_path = "crawl_wiktionary/macrons_wiktionary_test_format_nfc.tsv"
#process_wiktionary_entries(db_path, wiktionary_path)
