'''

For all nouns, Bailly abrégé has (ὁ)&nbsp; (ἡ)&nbsp; or (τό)&nbsp;
'''

import csv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm  # Import tqdm for the progress indicator
from greek_accentuation.characters import length
from concurrent.futures import ThreadPoolExecutor, as_completed

SHORT = '̆'
LONG = '̄'

# Function to get the macronized word from the LSJ website
def get_macronized_word(greek_word):
    url = f"https://lsj.gr/wiki/{greek_word}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        span_elements = soup.find_all('span', title="Look up on Google")
        if span_elements:
            word = span_elements[0].get_text()
            return word
    return None

def has_macron_or_breve(word):
    if word:
        for char in word:
            if length(char) in [SHORT, LONG]:
                return True
    return False

def process_row(row):
    if len(row) == 3:
        token, tag, lemma = row
        macronized_word = get_macronized_word(token)
        # Check if macronized_word has macron or breve
        if macronized_word and has_macron_or_breve(macronized_word):
            return row + [macronized_word]
    return row

def process_file(input_file_path, output_file_path, max_workers=10):
    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
         open(output_file_path, 'w', encoding='utf-8', newline='') as output_file:
        reader = csv.reader(input_file, delimiter='\t')
        writer = csv.writer(output_file, delimiter='\t')

        # Convert reader to a list for accurate tqdm progress tracking
        rows = list(reader)
        
        # Initialize ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all rows for processing
            future_to_row = {executor.submit(process_row, row): row for row in rows}
            
            # Initialize tqdm progress bar
            for future in tqdm(as_completed(future_to_row), total=len(rows), desc="Processing", unit="lines"):
                result = future.result()
                writer.writerow(result)

# Example usage
input_file_path = "prepare_tokens/tokens/tokens.tsv"  # Path to your input file
output_file_path = "crawl_lsj/macrons_lsj_raw.txt"  # Path where you want to save the output file
process_file(input_file_path, output_file_path)
