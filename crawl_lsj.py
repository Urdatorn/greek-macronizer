import csv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm  # Import tqdm for the progress indicator
from greek_accentuation.characters import length

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

def process_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
         open(output_file_path, 'w', encoding='utf-8', newline='') as output_file:
        reader = csv.reader(input_file, delimiter='\t')
        writer = csv.writer(output_file, delimiter='\t')
        
        # Wrap reader with tqdm to show progress bar
        for row in tqdm(reader, desc="Processing", unit="lines"):
            if len(row) == 3:
                token, tag, lemma = row
                macronized_word = get_macronized_word(token)
                # Check if macronized_word has macron or breve
                if macronized_word and has_macron_or_breve(macronized_word):
                    output_row = row + [macronized_word]
                else:
                    output_row = row
                writer.writerow(output_row)
            else:
                writer.writerow(row)

# Example usage
input_file_path = "prepare_tokens/tokens/tokens_no_duplicates.txt"  # Path to your input file
output_file_path = "crawl_lsj/macrons_lsj.txt"  # Path where you want to save the output file
process_file(input_file_path, output_file_path)
