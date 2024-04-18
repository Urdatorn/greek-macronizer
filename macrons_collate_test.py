import csv
import unicodedata

def collate_two_tsv(base_tsv_path, added_tsv_path, output_tsv_path):
    # Load the entries from added_tsv into a dictionary for fast lookup
    added_entries = {}
    with open(added_tsv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            key = unicodedata.normalize('NFC', row[0].strip())
            added_entries[key] = row[1].strip()

    # Process base_tsv and append data from added_tsv where appropriate
    with open(base_tsv_path, 'r', encoding='utf-8') as base_file, \
         open(output_tsv_path, 'w', newline='', encoding='utf-8') as output_file:
        reader = csv.reader(base_file, delimiter='\t')
        writer = csv.writer(output_file, delimiter='\t')
        
        unmatched = []  # List to store unmatched entries for diagnostics

        for base_row in reader:
            # Normalize and strip whitespace
            token = unicodedata.normalize('NFC', base_row[0].strip())
            
            if token in added_entries:
                # Match found, append the corresponding value and "wiktionary"
                base_row.append(added_entries[token])
                base_row.append("wiktionary")
            else:
                # No match found, append empty fields for consistency
                unmatched.append(base_row[0])
                base_row.extend(['', ''])

            writer.writerow(base_row)

    # Print or log unmatched entries for review
    print("Unmatched entries:", unmatched)


# Example usage:
collate_two_tsv('macrons_test.tsv', 'macrons_test_added.tsv', 'macrons_test_result.tsv')
