import concurrent.futures
from bs4 import BeautifulSoup
import os
import sqlite3
from tqdm import tqdm

def create_database(db_path):
    """
    Creates a SQLite database with the necessary table for storing tokens and their metrical patterns.
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS metrical_patterns (
            id INTEGER PRIMARY KEY,
            token TEXT NOT NULL,
            metrical_pattern TEXT NOT NULL
        )
        ''')
        conn.commit()
    print("Database created and initialized.")

def process_html_file(file_path, db_path):
    """
    Processes a single HTML file, extracts metrical patterns, and inserts them into the database.
    Each thread uses its own database connection.
    """
    word_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    
    for word_div in soup.find_all(class_="word"):
        syllables = [(syll.text, 'long' if 'long' in syll.get('class', []) else 'short') for syll in word_div.find_all('span')]
        reconstructed_word = ''.join(syll[0] for syll in syllables)
        formatted_syllables = [[syll[0], '_' if syll[1] == 'long' else '^'] for syll in syllables]
        metrical_pattern = ','.join([''.join(pair) for pair in formatted_syllables])
        word_data.append((reconstructed_word, metrical_pattern))
    
    # Insert data into the database
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.executemany('INSERT INTO metrical_patterns (token, metrical_pattern) VALUES (?, ?)', word_data)
        conn.commit()

def preprocess_html_files_and_store_parallel(folder_path, db_path):
    """
    Processes HTML files in parallel to store metrical patterns using individual database connections for each thread.
    """
    html_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.html')]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_html_file, file_path, db_path) for file_path in html_files]
        # Use tqdm to display progress
        for _ in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing HTML files in parallel"):
            pass

db_path = 'crawl_hypotactic/metrical_patterns.db'
folder_path = 'crawl_hypotactic/hypotactic_htmls_greek'

create_database(db_path)  # Ensure the database is initialized before processing
preprocess_html_files_and_store_parallel(folder_path, db_path)
