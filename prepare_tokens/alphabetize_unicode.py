'''
Alphabetizing a polytonic Greek dictionary after token and then lemma. 

For porting the Unicode Collation Algorithm to python, see:
https://github.com/jtauber/pyuca
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import csv
from pyuca import Collator
from utils import Colors

def sort_greek_file(input_file_path, output_file_path):
    c = Collator()

    with open(input_file_path, 'r', encoding='utf-8') as infile:
        rows = list(csv.reader(infile, delimiter='\t'))

    sorted_rows = sorted(rows, key=lambda row: (c.sort_key(row[2]), c.sort_key(row[0])) if len(row) >= 3 else ('', ''))

    with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerows(sorted_rows)

    print(f"{Colors.GREEN}Sorted file saved to {output_file_path}{Colors.ENDC}")

def main():
    input_file_path = 'macrons_alg3_prefix2.tsv'  # Adjust as necessary
    output_file_path = 'macrons_alg3_prefix2.tsv'  # Adjust as necessary

    sort_greek_file(input_file_path, output_file_path)

if __name__ == "__main__":
    main()
