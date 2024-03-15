'''
1) Collating all sources of macrons into a single db, in order of precedence:
    - manual
    - LSJ
    - Ifthimos
    - Hypotactic

A token will be macronized according to the highest source it appears in,
and not overwritten if it appears in a subsequent source.

2) Using the macronized entries, we try to fill in the remaining ones by extrapolation.
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

The db has columns:
token, tag, lemma, macrons, pos, source


'''
import sqlite3
import csv
from utils import Colors



def create_output_database(db_path="macrons.db"):
    """
    Creates the output database called 'macrons' for storing tokens along with tag, lemma, macrons, pos, and source.
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS annotated_tokens (
            id INTEGER PRIMARY KEY,
            token TEXT NOT NULL,
            tag TEXT,
            lemma TEXT,
            macrons TEXT,
            pos TEXT,
            source TEXT
        )
        ''')
        conn.commit()
    print("Database and table created successfully.")

# Call the function to create the database and table
create_output_database()


def populate_db_with_tokens_and_pos(db_path, tokens_path, pos_path):
    # Step 1: Load all lines from pos_path into a dictionary for quick lookup
    # The key will be the tuple of (token, tag, lemma) for quick matching
    pos_mapping = {}
    with open(pos_path, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if len(row) >= 4:
                key = tuple(row[1:4])  # Using columns 2-4 as the key
                pos_mapping[key] = row[0]  # First column is the POS

    # Step 2: Open the database connection and prepare for data insertion
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    total_lines, lines_with_pos = 0, 0
    with open(tokens_path, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            total_lines += 1
            if len(row) >= 3:
                # Form the key from the current row for lookup in pos_mapping
                key = tuple(row)
                pos = pos_mapping.get(key, None)
                if pos:
                    lines_with_pos += 1
                    # Prepare the insert statement with the POS column included
                    cursor.execute('''INSERT INTO annotated_tokens (token, tag, lemma, pos) 
                                      VALUES (?, ?, ?, ?)''', (*key, pos))

    # Commit changes and close the database connection
    conn.commit()
    conn.close()

    print(f"Total lines processed: {total_lines}")
    print(f"Lines with POS matched and inserted: {lines_with_pos}")
    if total_lines == lines_with_pos:
        print("All lines successfully matched with POS information.")
    else:
        print("Some lines did not match any POS information. Check for unmatched cases.")

# Example function call
populate_db_with_tokens_and_pos("macrons.db", "prepare_tokens/tokens/tokens.txt", "prepare_tokens/tokens/tragedies_300595_pos_norm.txt")



def print_ascii_art():
    cyan = Colors.CYAN
    endc = Colors.ENDC

    print(cyan + "                                           _        _   " + endc)
    print(cyan + " _ __ ___   __ _  ___ _ __ ___  _ __  ___ | |___  _| |_ " + endc)
    print(cyan + "| '_ ` _ \\ / _` |/ __| '__/ _ \\| '_ \\/ __|| __\\ \\/ / __|" + endc)
    print(cyan + "| | | | | | (_| | (__| | | (_) | | | \\__ \\| |_ >  <| |_ " + endc)
    print(cyan + "|_| |_| |_|\\__,_|\\___|_|  \\___/|_| |_|___(_)__/_/\\_\\__|" + endc)

#print_ascii_art()
#print(f"{Colors.CYAN} Starting to prepare macrons.txt!{Colors.ENDC}")