'''
We want to generalize macrons so that given say

    μεγίστας	a-p---fa-	μέγας	_7	ifthimos
    μέγιστε	a-s---mvs	μέγας		
    μεγίστη	a-s---fn-	μέγας		
    μεγίστην	a-s---fas	μέγας		
    μεγίστης	a-s---fgs	μέγας		
    μέγιστον	a-s---nas	μέγας	^4	wiktionary

all lines inherit the breve iota ^4 from the last line. 

Suggestion: if two lines share lemma and their tokens differ only wrt the final syllable,
then they should share all macrons referring to earlier syllables. 

'''

from utils import Colors, only_bases
from erics_syllabifier import syllabifier


def ultima(word):
    '''
    >> ultima('ποτιδέρκομαι')
    >> μαι
    '''
    list_of_syllables = syllabifier(word)
    ultima = list_of_syllables[-1]

    return ultima


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