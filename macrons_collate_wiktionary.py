import sqlite3
import csv
import logging
from utils import Colors
from tqdm import tqdm


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


print(count_equivalent_entries('prepare_tokens/tokens/tokens.txt', 'macrons.db', 'annotated_tokens', 'token'))


###


# Initialize logging
logging.basicConfig(filename='macrons_update.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_existing_macrons(cursor, token):
    """Fetch the existing macrons for a given token from the database."""
    cursor.execute("SELECT macrons FROM annotated_tokens WHERE token = ?", (token,))
    result = cursor.fetchone()
    return result[0] if result else None

def ordinal_in_existing(existing_macrons, new_macron):
    """Check if the ordinal of the new macron exists in the existing macrons string."""
    if existing_macrons:
        existing_ordinals = [int(''.join(filter(str.isdigit, macron))) for macron in existing_macrons.split(',')]
        new_ordinal = int(''.join(filter(str.isdigit, new_macron)))
        return new_ordinal in existing_ordinals
    return False

def insert_macron_in_order(existing_macrons, new_macron):
    """Insert the new macron into the existing macrons string in the correct ordinal position."""
    if not existing_macrons:
        return new_macron
    existing_list = existing_macrons.split(',')
    new_ordinal = int(''.join(filter(str.isdigit, new_macron)))
    for i, macron in enumerate(existing_list):
        ordinal = int(''.join(filter(str.isdigit, macron)))
        if new_ordinal < ordinal:
            existing_list.insert(i, new_macron)
            break
    else:
        existing_list.append(new_macron)
    return ','.join(existing_list)

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
        total_lines = sum(1 for _ in file)
        file.seek(0)  # Reset file pointer after counting lines

        for line in tqdm(reader, total=total_lines, desc="Processing Wiktionary entries"):
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
#db_path = "macrons_wiktionary.db"
#wiktionary_path = "crawl_wiktionary/macrons_wiktionary.txt"
#process_wiktionary_entries(db_path, wiktionary_path)
