'''
Create a tsv dictionary from ifthimos with the raw unformatted macron info
'''

import csv
import subprocess
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


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
        if output == "No match":
            #print(f"No macronization information found for {token}")
            return ''
        else:
            return output
    else:
        print("Error calling ifthimos_macronizer:", result.stderr)
        return ''

#token = 'εὐδρακής'
#pos = 'a-s---mn-'
#print(call_ifthimos_macronizer(token, pos))

#token = 'ἄγνυμι'
#pos = 'v1spia---'
#print(call_ifthimos_macronizer(token, pos))


def process_row(row):
    '''
    Process a single row from the TSV file.
    If the row has fewer than 4 columns, it appends empty strings to ensure there is space for the macron.
    '''
    # Ensure the row has at least 4 columns
    while len(row) < 4:
        row.append('')  # Append empty strings if fewer than 4 columns exist

    if len(row) >= 3:
        token, tag, lemma = row[0], row[1], row[2]
        macron = call_ifthimos_macronizer(token, tag)
        row[3] = macron  # Set macron explicitly in the fourth column

    return row


def process_tsv(input_file_path, output_file_path, max_workers=10):
    '''
    Process a TSV file to add macron information using the ifthimos macronizer with parallel processing.
    Reads the file using csv, processes each row with parallelization, except for the header,
    and then writes the modified rows back to a new TSV file including the unmodified header.
    '''
    with open(input_file_path, 'r', encoding='utf-8', newline='') as infile:
        reader = csv.reader(infile, delimiter='\t')
        header = next(reader)  # Read the first line separately as the header
        rows = list(reader)  # Read the rest of the data

    # Initialize ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Wrap the executor with tqdm for progress bar
        results = list(tqdm(executor.map(process_row, rows), total=len(rows), desc="Processing rows"))

    # Write results to output file, including the header
    with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerow(header)  # Write the header first
        for row in results:
            writer.writerow(row)


# Example usage
input_tsv_path = 'macrons_empty.tsv'  # Path to your input TSV file
output_tsv_path = 'macrons_ifthimos_raw.tsv'  # Path to the output TSV file
process_tsv(input_tsv_path, output_tsv_path)