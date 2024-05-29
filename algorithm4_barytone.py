'''
Barytones inherit their macra from oxytones

'''
import re
import csv

from utils import Colors, only_bases, graves, acutes
from erics_syllabifier import syllabifier


def ultima(word):
    '''
    >> ultima('ποτιδέρκομαι')
    >> μαι
    '''
    list_of_syllables = syllabifier(word)
    ultima = list_of_syllables[-1]

    return ultima


def barytone(token):
    graves = r'[ὰὲὴὶὸὺὼῒῢἂἃἒἓἢἣἲἳὂὃὒὓὢὣᾂᾃᾲᾒᾓῂᾢᾣῲ]'
    if re.search(graves, token):
        return True
    return False


def should_share_macrons(line1, line2):
    columns1 = line1.split('\t')
    columns2 = line2.split('\t')

    token_1, tag_1, lemma_1, macron_1 = columns1[:4]
    token_2, tag_2, lemma_2, macron_2 = columns2[:4]

    list_of_syllables1 = syllabifier(token_1)
    list_of_syllables2 = syllabifier(token_2)

    except_ultima1 = list_of_syllables1[:-1]
    except_ultima2 = list_of_syllables2[:-1]

    return except_ultima1 and except_ultima2 and lemma_1 == lemma_2 and only_bases(except_ultima1) == only_bases(except_ultima2)

print(should_share_macrons('μεγίστης	a-s---fgs	μέγας		','μέγιστον	a-s---nas	μέγας	^4	wiktionary'))


def replace_grave_with_acute(token):
    '''
    >>> replace_grave_with_acute('ἱεὶς')
    >>> ἱείς
    '''
    def replace(match):
        char = match.group(0)
        pos = graves.index(char)
        return acutes[pos]
    
    return re.sub(graves, replace, token)


def macronize_barytones(input_tsv, output_tsv):
    print('hello world')
    lines = []
    barytones_macronized = 0
    
    # Read the input TSV file
    with open(input_tsv, mode='r', encoding='utf-8', newline='') as infile:
        reader = csv.reader(infile, delimiter='\t')
        lines = [row for row in reader]

    # Create a dictionary for quick lookup
    token_to_macron = {}
    for row in lines:
        if row and len(row) >= 4:
            token_in, tag_in, lemma_in, macron_in = row[:4]
            source_in = row[4] if len(row) > 4 else ''
            token_to_macron[token_in] = (macron_in, source_in)

    # Process each line
    for row in lines:
        if row and len(row) >= 4:
            token_in, tag_in, lemma_in, macron_in = row[:4]
            source_in = row[4] if len(row) > 4 else ''
            
            if barytone(token_in):
                acute_token = replace_grave_with_acute(token_in)
                if acute_token in token_to_macron:
                    macron_out, source_out = token_to_macron[acute_token]
                    row[3] = macron_out
                    if 'barytone' not in source_in:
                        row[4] = f"{source_in},barytone" if source_in else "barytone"
                    barytones_macronized += 1
                else:
                    row[4] = source_in

    # Write the updated lines to the output TSV file
    with open(output_tsv, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerows(lines)

    # Print summary information
    print(f"{Colors.GREEN}Processed file saved as: {output_tsv}{Colors.ENDC}")
    print(f"{Colors.GREEN}Total number of barytones macronized: {barytones_macronized}{Colors.ENDC}")


input_tsv = 'macrons_alg3_prefix2.tsv'
output_tsv = 'macrons_alg4_barytone.tsv'
macronize_barytones(input_tsv, output_tsv)