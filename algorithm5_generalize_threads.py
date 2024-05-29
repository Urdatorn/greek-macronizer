'''
For tokens with 
    i) >2 syllables 
    ii) sharing lemma and
    iii) differing only wrt the ultima,
 we want to generalize macra so that given say

    μεγίστας	a-p---fa-	μέγας	_7	ifthimos
    μέγιστε	a-s---mvs	μέγας		
    μεγίστη	a-s---fn-	μέγας		
    μεγίστην	a-s---fas	μέγας		
    μεγίστης	a-s---fgs	μέγας		
    μέγιστον	a-s---nas	μέγας	^4	wiktionary

all lines inherit the breve iota ^4 from the last line. 

First run:
Finished 29 May, ran for 49:28:44
Total number of cognates with updated macron columns: 4630

'''
import re
import csv

from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import Colors, only_bases, graves, acutes
from erics_syllabifier import syllabifier

from algorithm1_accentual_rules import ordinal_last_vowel
from collate_macrons import collate_macrons


def ultima(word):
    '''
    >> ultima('ποτιδέρκομαι')
    >> μαι
    '''
    list_of_syllables = syllabifier(word)
    ultima = list_of_syllables[-1]

    return ultima


def should_share_macrons(line1, line2):
    '''
    >>> line1 = 'μεγίστης	a-s---fgs	μέγας		'
    >>> line2 = 'μέγιστον	a-s---nas	μέγας	^4	wiktionary'
    >>> should_share_macrons(line1, line2)
    >>> True
    '''
    columns1 = line1.split('\t')
    columns2 = line2.split('\t')

    token_1, tag_1, lemma_1, macron_1 = columns1[:4]
    token_2, tag_2, lemma_2, macron_2 = columns2[:4]

    list_of_syllables1 = syllabifier(token_1)
    list_of_syllables2 = syllabifier(token_2)

    except_ultima1 = list_of_syllables1[:-1]
    except_ultima2 = list_of_syllables2[:-1]

    return len(token_1) > 2 and len(token_2) > 2 and except_ultima1 and except_ultima2 and lemma_1 == lemma_2 and only_bases(except_ultima1) == only_bases(except_ultima2)


def process_pairs(data_lines, start, end):
    cognates = 0
    for i in tqdm(range(start, end), desc="Processing chunk", leave=False):
        line1 = data_lines[i]
        if len(line1) < 4:
            continue

        token_1, tag_1, lemma_1, macron_1 = line1[:4]
        source_1 = line1[4] if len(line1) > 4 else ''

        for j in range(i + 1, len(data_lines)):
            line2 = data_lines[j]
            if len(line2) < 4:
                continue

            token_2, tag_2, lemma_2, macron_2 = line2[:4]
            source_2 = line2[4] if len(line2) > 4 else ''

            if should_share_macrons('\t'.join(line1), '\t'.join(line2)):
                macron_count_1 = len(re.findall(r'[\^_]\d+', macron_1))
                macron_count_2 = len(re.findall(r'[\^_]\d+', macron_2))

                if macron_count_1 > macron_count_2:
                    last_vowel_pos_1 = ordinal_last_vowel(token_1)
                    updated_macron_2 = collate_macrons(macron_2, macron_1)

                    line2[3] = updated_macron_2
                    if 'cognate' not in source_2:
                        line2[4] = f"{source_2},cognate" if source_2 else "cognate"
                    cognates += 1
    return cognates

def macronize_cognates(input_tsv, output_tsv, num_workers=4):
    lines = []
    total_cognates = 0
    
    # Read the input TSV file
    with open(input_tsv, mode='r', encoding='utf-8', newline='') as infile:
        reader = csv.reader(infile, delimiter='\t')
        lines = [row for row in reader]

    if not lines:
        print(f"{Colors.RED}Error: The file {input_tsv} is empty or invalid.{Colors.ENDC}")
        return

    # Skip the header line
    header = lines[0]
    data_lines = lines[1:]

    # Partition the data
    chunk_size = len(data_lines) // num_workers
    chunks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_workers)]
    chunks[-1] = (chunks[-1][0], len(data_lines))  # Ensure the last chunk goes to the end

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(process_pairs, data_lines, start, end) for start, end in chunks]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing chunks", unit="chunk"):
            total_cognates += future.result()

    # Write the updated lines to the output TSV file
    with open(output_tsv, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerow(header)
        writer.writerows(data_lines)

    # Print summary information
    print(f"{Colors.GREEN}Processed file saved as: {output_tsv}{Colors.ENDC}")
    print(f"{Colors.GREEN}Total number of cognates with updated macron columns: {total_cognates}{Colors.ENDC}")


input_tsv = 'macrons_alg4_barytone.tsv'
output_tsv = 'macrons_alg5_generalize_threads.tsv'
macronize_cognates(input_tsv, output_tsv)
