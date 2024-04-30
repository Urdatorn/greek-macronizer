import sqlite3
import csv
import subprocess
from tqdm import tqdm
from greek_accentuation.characters import length, strip_length



def create_macrons_ifthimos_database(db_path="macrons_hypotactic.db"):
    '''
    Creates a SQLite database with the necessary table for storing tokens and their macronization information.
    '''
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS annotated_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL,
            macrons TEXT
        )
        ''')
        conn.commit()
    print("Database created and table set up.")


def call_ifthimos_macronizer(token, pos):
    '''
    >>token = 'ἄγνυμι'
    >>pos = 'v1spia---'
    >>call_ifthimos_macronizer(token, pos)
    >>ῡ
    '''
    ifthimos_folder_path = 'ifthimos'
    # Adjust the command to call the Ruby script from within its directory
    command = ['ruby', 'macronize.rb', token, pos]
    # Use the cwd parameter to set the current working directory to the ifthimos subfolder
    result = subprocess.run(command, capture_output=True, text=True, cwd=ifthimos_folder_path)

    if result.returncode == 0:
        output = result.stdout.strip()
        # Check for "No match" output and handle accordingly
        if output == "No match":
            print(f"No macronization information found for {token}")
            return None
        else:
            return output
    else:
        print("Error calling ifthimos_macronizer:", result.stderr)
        return None


SHORT = '̆'
LONG = '̄'

# Define length_count as a global dictionary
length_count = {'long': 0, 'short': 0}

def separate_macrons_from_word(word):
    '''
    >>separate_macrons_from_word('νεᾱνῐ́ᾱς')
    >>('νεανίας', ['_3', '^5', '_7'])
    '''
    global length_count  # Declare length_count as global to modify it
    processed_word = ""
    modifications = []
    i = 1  # Initialize character position counter
    for char in word:
        char_length = length(char)
        if char_length == LONG:
            processed_char = strip_length(char)
            modifications.append(f"_{i}")
            length_count['long'] += 1
        elif char_length == SHORT:
            processed_char = strip_length(char)
            modifications.append(f"^{i}")
            length_count['short'] += 1
        else:
            processed_char = char

        processed_word += processed_char
        if char != SHORT and char != LONG:
            i += 1

    return processed_word, modifications


def populate_db(db_path, tokens_file_path):
    # First, count the total number of lines in the tokens file for tqdm
    with open(tokens_file_path, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)

    # Now, process each line with tqdm for progress indication
    with sqlite3.connect(db_path) as conn, open(tokens_file_path, 'r', encoding='utf-8') as file:
        cursor = conn.cursor()
        reader = csv.reader(file, delimiter='\t')

        # Wrap the reader with tqdm for progress indication
        for row in tqdm(reader, total=total_lines, desc="Processing tokens"):
            if len(row) >= 2:  # Ensure there is both a token and a POS
                token, pos = row[0], row[1]
                macronized_output = call_ifthimos_macronizer(token, pos)
                if macronized_output:
                    _, macrons = separate_macrons_from_word(macronized_output)
                    macrons_str = ''.join(macrons)
                else:
                    macrons_str = None

                cursor.execute('''INSERT INTO annotated_tokens (token, macrons) VALUES (?, ?)''', (token, macrons_str))
        conn.commit()


# Example function calls
create_macrons_ifthimos_database()
populate_db("macrons_hypotactic.db", "prepare_tokens/tokens/tokens.txt")


# Example usage
#token = 'ἄγνυμι'
#pos = 'v1spia---'
#macronized = call_ifthimos_macronizer(token, pos)
#print(separate_macrons_from_word(macronized))
