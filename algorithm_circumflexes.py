'''
Algorithm for macronizing all circumflexes

Test input May 1:

χαρακτήρ	n-s---mn-	χαρακτήρ	^2	wiktionary
σφραγῖδα	n-s---fa-	σφραγίς	_4_6^8	ifthimos
σφραγῖδα	n-s---fa-	σφραγίς	_4^8	ifthimos
σφραγῖδα	n-s---fa-	σφραγίς	_4^8	

Test result:

χαρακτήρ	n-s---mn-	χαρακτήρ	^2	wiktionary
σφραγῖδα	n-s---fa-	σφραγίς	_4_6^8	ifthimos
σφραγῖδα	n-s---fa-	σφραγίς	_4_6^8	ifthimos,circumflex
σφραγῖδα	n-s---fa-	σφραγίς	_4_6^8	circumflex

'''

import csv
import re
import unicodedata

from greek_accentuation.characters import base

from utils import Colors, base_alphabet, circumflexes
from collation.macrons_collate_lsj import ordinal_in_existing, collate_macrons
from erics_syllabifier import patterns


def macronize_circumflexes(word):
    '''
    Returns a list of strings of formatted macrons for every circumflex in a word
    >>> macronize_circumflexes('σφραγῖδα')
    >>> ['_6']
    If there are no circumflexes, an empty list [] is returned.
    To avoid confusing macronizations of iotas in diphthongs like
        ἀγγεῖλαι	v--ana---	ἀγγέλλω	_5	circumflex
    we use a regex stoplist.
    '''
    diphth_i = r'(α|ε|ο|υ)(ἰ|ί|ι|ῖ|ἴ|ἶ|ἵ|ἱ|ἷ|ὶ|ἲ|ἳ)'
    modifications = []
    i = 1  # Human-readable character position counter
    skip_next = False  # Flag to skip next character if it's part of a diphthong

    # Preprocess to find all matches for diphth_i
    diphthongs = [(match.start(), match.end()) for match in re.finditer(diphth_i, word, re.UNICODE)]

    for idx, char in enumerate(word):
        if re.search(base_alphabet, base(char)):
            # Check if the character is part of any diphthong we need to skip
            if any(start <= idx < end for start, end in diphthongs):
                if base(char) == 'ι':
                    # Skip this index because it's an iota in a diphthong
                    skip_next = True
                    continue

            if char in circumflexes and not skip_next:
                modifications.append(f"_{i}")
            skip_next = False  # Reset skip flag
            i += 1

    return modifications


def macronize_circumflexes_in_tsv(input_tsv, output_tsv):
    updated_source_count = 0
    
    with open(input_tsv, mode='r', encoding='utf-8', newline='') as infile, \
         open(output_tsv, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')
        
        for row in reader:
            if row and len(row) >= 4:
                token_in, tag_in, lemma_in, macron_in = row[:4]
                source_in = row[4] if len(row) > 4 else ''
                
                normalized_token = unicodedata.normalize('NFC', token_in)
                new_macrons = macronize_circumflexes(normalized_token)
                new_macron_str = ''.join(new_macrons)
                new_macron_parts = re.findall(r'[\^_]\d+', new_macron_str)
                
                should_update_source = False
                for macron in new_macron_parts:
                    if not ordinal_in_existing(macron_in, macron):
                        should_update_source = True
                        break
                
                if should_update_source:
                    macron_out = collate_macrons(macron_in, new_macron_str)
                    source_out = f"{source_in},circumflex" if source_in else "circumflex"
                    updated_source_count += 1
                else:
                    macron_out = macron_in
                    source_out = source_in
                
                output_row = [token_in, tag_in, lemma_in, macron_out, source_out]
                writer.writerow(output_row)
    
    print(f"{Colors.GREEN}Number of lines with updated source: {updated_source_count}{Colors.ENDC}")


if __name__ == '__main__':
    #input_tsv = 'test_files/macrons_test_circumflex.tsv'
    #output_tsv = 'test_files/macrons_test_circumflex_result.tsv'
    input_tsv = 'macrons_wiki_hypo_ifth_lsj.tsv'
    output_tsv = 'macrons_alg1_circumflex.tsv'
    macronize_circumflexes_in_tsv(input_tsv, output_tsv)

'''
Using the above functions as specified below, make a function macronize_circumflexes_in_tsv(input_tsv, output_tsv).
For the input rows, use the naming convention 
            if row and len(row) >= 4:
                token_in, tag_in, lemma_in, macron_in = row[:4]
                source_in = row[4] if len(row) > 4 else ''
and the same for the out row but wth token_out, etc. 

Apply macronize_circumflexes to every token_in after having applied unicodedata.normalize NFC on it.
If the returned list is not an empty list []: 
(i) save the return as new_macrons. 
(ii) Then make macron_out = collate_macrons(macron_in, new_macrons), 
and write the result as the out fourth column and 
(iii) append (using comma-separation if there is a previous entry) source_in with 'circumflex',
calling the result source_out. The whole out tsv-line written will then be 
    token_in, tag_in, lemma_in, macron_out, source_out
If, however, macronize_circumflexes returns [], then just write the in line unchanged.
'''

