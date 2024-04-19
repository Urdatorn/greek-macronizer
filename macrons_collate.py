'''

Final step of the creation of the macron dictionary.

We start with macrons_empty.tsv, which is just a copy of tokens.tsv
The columns are referred to as token, tag, lemma, macron, source,
and the goal is to fill in the macron and source columns. 

    Step 1) Collating all sources of macrons into a single db, in order of quality precedence:
        - manual
        - LSJ (only lemmata, little/no pos)
        - Ifthimos (only endings, full pos compatibility)
        - Wiktionary (no pos)
        - Hypotactic (no pos)

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


# Configure logging
logging.basicConfig(filename='wiktionary_update.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def collate_wiktionary(db_path, wiktionary_path):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Read the total lines for progress indication
    with open(wiktionary_path, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)

    # Variables to keep track of updates
    macrons_written = 0
    macrons_skipped = 0

    # Read and process the Wiktionary file
    with open(wiktionary_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        
        for line in tqdm(reader, total=total_lines, desc="Processing Wiktionary entries"):
            if len(line) >= 2:
                token, macrons = line[0], line[1]
                
                # Check if the macrons column is empty for the token
                cursor.execute("SELECT macrons FROM annotated_tokens WHERE token = ?", (token,))
                result = cursor.fetchone()
                
                if result and (result[0] is None or result[0] == ''):  # Correct grouping with parentheses
                    # Update the macrons column and set source to 'wiktionary'
                    cursor.execute("UPDATE annotated_tokens SET macrons = ?, source = 'wiktionary' WHERE token = ?", (macrons, token))
                    conn.commit()
                    macrons_written += 1
                else:
                    macrons_skipped += 1

    # Close the database connection
    conn.close()

    # Log and print the summary
    logging.info(f"Macrons written: {macrons_written}")
    logging.info(f"Macrons skipped (already present): {macrons_skipped}")
    print(f"{Colors.GREEN}Macrons written: {macrons_written}{Colors.ENDC}")
    print(f"{Colors.RED}Macrons skipped (already present): {macrons_skipped}{Colors.ENDC}")

def main():
    print_ascii_art()
    
    db_path = 'macrons.db'  # Path to your SQLite database
    wiktionary_path = 'crawl_wiktionary/macrons_wiktionary.txt'  # Path to the Wiktionary TSV file
    collate_wiktionary(db_path, wiktionary_path)

if __name__ == "__main__":
    main()
