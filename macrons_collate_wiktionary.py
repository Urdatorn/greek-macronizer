import csv
import logging
import unicodedata
from tqdm import tqdm
from utils import Colors, all_vowels, with_spiritus, only_bases

# Setup logging configuration
logging.basicConfig(filename='macrons_collate_wiktionary.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def collate_two_tsv(base_tsv_path, added_tsv_path, output_tsv_path):
    # Load the entries from added_tsv into a dictionary for fast lookup
    added_entries = {}
    with open(added_tsv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if row:  # Ensure the row is not empty
                key = unicodedata.normalize('NFC', row[0].strip())
                added_entries[key] = row[1].strip()

    matching_lines = 0
    unmatched_lines = 0

    # Process base_tsv and append data from added_tsv where appropriate
    with open(base_tsv_path, 'r', encoding='utf-8') as base_file, \
         open(output_tsv_path, 'w', newline='', encoding='utf-8') as output_file:
        reader = csv.reader(base_file, delimiter='\t')
        writer = csv.writer(output_file, delimiter='\t')

        for base_row in tqdm(reader, desc="Collating with Wiktionary"):
            if base_row:  # Process only non-empty rows
                token = unicodedata.normalize('NFC', base_row[0].strip())
                
                if token in added_entries:
                    # Match found, append the corresponding value and "wiktionary"
                    base_row.append(added_entries[token])
                    base_row.append("wiktionary")
                    matching_lines += 1
                else:
                    # No match found, append empty fields for consistency
                    base_row.extend(['', ''])
                    unmatched_lines += 1

                writer.writerow(base_row)

    # Log the results
    logging.info(f"{Colors.GREEN}Total matching lines: {matching_lines}{Colors.ENDC}")
    logging.info(f"{Colors.RED}Total unmatched lines: {unmatched_lines}{Colors.ENDC}")
    print(f"{Colors.GREEN}Total matching lines: {matching_lines}{Colors.ENDC}")
    print(f"{Colors.RED}Total unmatched lines: {unmatched_lines}{Colors.ENDC}")

# Example usage:
collate_two_tsv('macrons_empty.tsv', 'crawl_wiktionary/macrons_wiktionary.tsv', 'macrons_wiki_collated.tsv')
