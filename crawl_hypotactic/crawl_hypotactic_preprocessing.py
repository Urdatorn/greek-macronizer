# IMPORTS


# Append the root folder to sys.path to be able to import from /utils.py and /erics_syllabifier.py
# Assuming your script is in a subfolder one level deep from the root
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sqlite3
import concurrent.futures
import logging
import re
from bs4 import BeautifulSoup
from tqdm import tqdm  # Import tqdm for the progress bar

from erics_syllabifier import patterns, syllabifier
from utils import Colors, DICHRONA, all_vowels # /utils.py


def create_database(db_path):
    # Connect to the SQLite database. This will create the file if it doesn't exist
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create a table to store tokens and metrical patterns
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS metrical_patterns (
        id INTEGER PRIMARY KEY,
        token TEXT NOT NULL,
        metrical_pattern TEXT NOT NULL
    )
    ''')
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Specify your database path
db_path = 'metrical_patterns.db'
create_database(db_path)


def preprocess_html_files_and_store(folder_path, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    html_files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
    for filename in tqdm(html_files, desc="Preprocessing HTML files"):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            
            for word_div in soup.find_all(class_="word"):
                syllables = [(syll.text, 'long' if 'long' in syll.get('class', []) else 'short') for syll in word_div.find_all('span')]
                reconstructed_word = ''.join(syll[0] for syll in syllables)
                formatted_syllables = [[syll[0], '_' if syll[1] == 'long' else '^'] for syll in syllables]
                metrical_pattern = ','.join([''.join(pair) for pair in formatted_syllables])
                
                # Insert the token and its metrical pattern into the database
                cursor.execute('INSERT INTO metrical_patterns (token, metrical_pattern) VALUES (?, ?)', (reconstructed_word, metrical_pattern))
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

folder_path = 'crawl_hypotactic/hypotactic_htmls_greek'
preprocess_html_files_and_store(folder_path, db_path)
