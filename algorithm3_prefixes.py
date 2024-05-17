'''
ALGORITHMIC MACRONIZING PART 2

Make a function brevize_syn(word) such that 
if only_bases(word) starts with 'συν', then
return '^2'

May 8:
Total tokens updated by brevize_syn: 273

'''

import csv
import unicodedata

from utils import Colors, only_bases
from collate_macrons import collate_macrons


def brevize_syn(word):
    base_form = only_bases(word)
    if base_form.startswith('συν'):
        return '^2'
    return None

# Example usage
print(brevize_syn('συνεργάτης'))  # Outputs: ^2
print(brevize_syn('σύνδεσμος'))   # Outputs: ^2
print(brevize_syn('διασυνδέσεις'))  # Outputs: None


def macronize_prefixes(input_tsv, output_tsv):
    prefix_count = 0
    first_line = True  # Flag to identify the header

    with open(input_tsv, mode='r', encoding='utf-8', newline='') as infile, \
         open(output_tsv, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        for row in reader:
            if first_line:
                # Write the header unchanged
                writer.writerow(row)
                first_line = False
                continue

            if row and len(row) >= 4:
                token_in, tag_in, lemma_in, macron_in = row[:4]
                source_in = row[4] if len(row) > 4 else ''

                normalized_token = unicodedata.normalize('NFC', token_in)
                original_macron = macron_in

                # Apply brevize_syn to the token
                new_macron = brevize_syn(normalized_token)
                if new_macron:
                    macron_in = collate_macrons(macron_in, new_macron)
                    if macron_in != original_macron:
                        if 'prefix' not in source_in:
                            source_out = f"{source_in},prefix" if source_in else "prefix"
                        prefix_count += 1
                    else:
                        source_out = source_in
                else:
                    source_out = source_in

                # Write the updated row to the output TSV
                output_row = [token_in, tag_in, lemma_in, macron_in, source_out]
                writer.writerow(output_row)


    # Print statistics
    print(f"{Colors.GREEN}Total tokens updated by brevize_syn: {prefix_count}{Colors.ENDC}")


if __name__ == '__main__':
    input_tsv = 'macrons_alg2_nominal.tsv'
    output_tsv = 'macrons_alg3_prefix.tsv'
    macronize_prefixes(input_tsv, output_tsv)