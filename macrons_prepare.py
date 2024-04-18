'''

Creating and preparing macrons.db.

The output db has 5 columns:
token, tag, lemma, macrons, source

The last two are filled by macrons_collate.py.

'''
import sqlite3
import csv
from utils import Colors


def create_output_database(db_path="macrons.db"):
    """
    Creates the output database called 'macrons' for storing tokens along with tag, lemma, macrons, and source.
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
            source TEXT
        )
        ''')
        conn.commit()
    print("Database and table created successfully.")

# Call the function to create the database and table
create_output_database()

def populate_db_with_tokens(db_path, tokens_path):
    """
    Populates the database with data from the tokens text file.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    total_lines = 0
    with open(tokens_path, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            total_lines += 1
            if len(row) >= 3:
                # Insert the data into the database
                cursor.execute('''INSERT INTO annotated_tokens (token, tag, lemma) VALUES (?, ?, ?)''', (row[0], row[1], row[2]))

    # Commit changes and close the database connection
    conn.commit()
    conn.close()

    print(f"{Colors.GREEN}Total lines processed and inserted: {total_lines}{Colors.ENDC}")

# Example function call
populate_db_with_tokens("macrons.db", "prepare_tokens/tokens/tokens_nfc.tsv")
