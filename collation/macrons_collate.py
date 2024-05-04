'''

Final step of the creation of the macron dictionary.

We start with macrons_empty.tsv, which is just a copy of tokens.tsv
The columns are referred to as token, tag, lemma, macron, source,
and the goal is to fill in the macron and source columns. 

    Step 1) Collating all sources of macrons into a single db, in order of quality precedence:
        - LSJ (only lemmata, little/no pos)
        - Ifthimos (macrons_ifthimos.tsv) (only endings, full pos compatibility) => 
        - Wiktionary (no pos) => macrons_collate_wiktionary.py (older)
        - Hypotactic (no pos) => macrons_collate_hypotactic.py (best collation script)

    A token will be macronized according to the highest source it appears in,
    and not overwritten if it appears in a subsequent source.
    However, any unmacronized dichrona may be filled in by appending macrons.

    Step 2) Using the macronized entries, we try to fill in the remaining ones by extrapolation.
    For example, in the below situation 

    ψυχή	n-s---fn-	ψυχή	ψῡχή
    ψυχὴ	n-s---fv-	ψυχή
    ψυχὴ	n-s---fn-	ψυχή
    ψυχῇ	n-s---fd-	ψυχή
    ψυχῶν	n-p---fg-	ψυχή
    ψυχῆς	n-s---fg-	ψυχή

    we need to make sure, in general, that tokens with both the same lemma and pos/word class will share the same macrons,
    given that there no instances of the same lemma with different macrons. 
    However, cases such as 
        ἵσταμεν (^1^4) vs ἵσταμεν (_1^4)
    with identical lemmata and pos's, but one or more differnt tag letters and differnt macrons

Detailed statistics should be output:
    - number of unmacronized dichrona
    - number of unique tokens with unmacronized dichrona
    - number of unique lemmata with unmacronized dichrona
    - statistics by wordclass

I will consequently build a web interface which will show only entries with fewer macrons than dichrona.


'''

import sqlite3
import csv
import logging
from tqdm import tqdm
from utils import Colors


def print_ascii_art():
    cyan = Colors.CYAN
    endc = Colors.ENDC

    print(cyan + "                                               _ _     " + endc)
    print(cyan + " _ __ ___   __ _  ___ _ __ ___  _ __  ___   __| | |__  " + endc)
    print(cyan + "| '_ ` _ \\ / _` |/ __| '__/ _ \\| '_ \\/ __| / _` | '_ \\ " + endc)
    print(cyan + "| | | | | | (_| | (__| | | (_) | | | \\__ \\| (_| | |_) |" + endc)
    print(cyan + "|_| |_| |_|\\__,_|\\___|_|  \\___/|_| |_|___(_)__,_|_.__/ " + endc)




