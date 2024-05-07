'''
ALGORITHMIC MACRONIZING PART 2

See page 38 in CGCG for endings of nominal forms.

RULES

Nominal forms
#1D
Nom and ac and voc sing can be either, depending on whether or not it comes from ionian -η. Tricky
Acc pl => long α; however acc pl fem of 3D are short: so if lemma is clearly 1D, ending is long

#2D
Nom and acc pl (neut): => short α (the only dichronon; Same as neuter pl 3D.)

#3D
Dat sing: short ι (all datives on iota are short)
Acc sing (masc) => short α
Nom and acc pl (neut) => short α, i.e. if noun is masc or neut and ends on -α, that α is short
Dat pl: short ι; see dat sing.
Acc pl (masc) => short α. Cf. 1D acc pl.

This yields the following three fully generalizable rules:
    (1) for tokens in Acc pl fem (^n.p...fa.$) with lemma on η or α, ending -α is short
    (2) for masc and neutre nouns (^n.....[mn]..$), ending -α is short regardless of case
    (3) for dat (^n......d.$) tag d at 8), then ending -ι is short

'''

import re
import csv
import os
import sys
import unicodedata

from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import Colors, DICHRONA, only_bases, all_vowels
from erics_syllabifier import patterns
from prepare_tokens.filter_dichrona import ultima, properispomenon, proparoxytone
from collate_macrons import collate_macrons


from greek_inflexion_interface import get_stem


