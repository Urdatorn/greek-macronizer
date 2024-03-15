'''
Collating all sources of macrons into a single db:
    - Hypotactic
    - LSJ
    - Ifthimos
    - manual

The db has columns:
token, tag, lemma, macrons, pos, source
'''

from utils import Colors
import sqlite3


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


def print_ascii_art():
    cyan = Colors.CYAN
    endc = Colors.ENDC

    print(cyan + "                                           _        _   " + endc)
    print(cyan + " _ __ ___   __ _  ___ _ __ ___  _ __  ___ | |___  _| |_ " + endc)
    print(cyan + "| '_ ` _ \\ / _` |/ __| '__/ _ \\| '_ \\/ __|| __\\ \\/ / __|" + endc)
    print(cyan + "| | | | | | (_| | (__| | | (_) | | | \\__ \\| |_ >  <| |_ " + endc)
    print(cyan + "|_| |_| |_|\\__,_|\\___|_|  \\___/|_| |_|___(_)__/_/\\_\\__|" + endc)

print_ascii_art()
print(f"{Colors.CYAN} Starting to prepare macrons.txt!{Colors.ENDC}")