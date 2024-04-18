from greek_accentuation.characters import base
from utils import base_alphabet, all_vowels, with_spiritus
import re
import unicodedata




def lacks_spiritus(word):
    """
    Checks if the first character of the word is a vowel and
    if the word does not contain any characters with spiritus.
    """
    if re.match(all_vowels, word[0]) and not re.search(with_spiritus, word):
        return True  
    return False

#nfd_form = unicodedata.normalize('NFC', 'ἀναβλέψαισθε')
#print(lacks_spiritus(nfd_form))

def count_lacking_spiritus(tsv_file_path, output_file_path):
    count = 0
    with open(tsv_file_path, 'r', encoding='utf-8') as infile, \
         open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            entry = line.strip().split('\t')[0]
            if entry and lacks_spiritus(entry):
                count += 1
                outfile.write(line)  # Write the satisfying line to the output file

    return count

# Example usage:
tsv_file_path = 'crawl_wiktionary/macrons_wiktionary_nfc.tsv'
output_file_path = 'crawl_wiktionary/macrons_wiktionary_no_spiritus.tsv'
total_entries_lacking_spiritus = count_lacking_spiritus(tsv_file_path, output_file_path)
print(f'Total entries lacking spiritus: {total_entries_lacking_spiritus}')