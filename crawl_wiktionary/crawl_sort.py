'''
Alphabetizing a polytonic Greek dictionary based on the first column.

For porting the Unicode Collation Algorithm to python, see:
https://github.com/jtauber/pyuca
'''

import csv
from pyuca import Collator


def sort_file(input_file_path, output_file_path):
    c = Collator()

    with open(input_file_path, 'r', encoding='utf-8') as infile:
        rows = list(csv.reader(infile, delimiter='\t'))

    # Sorting based solely on the first column
    sorted_rows = sorted(rows, key=lambda row: c.sort_key(row[0]) if len(row) > 0 else '')

    with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerows(sorted_rows)

    print(f"Sorted file saved to {output_file_path}")

def main():
    input_file_path = 'your_input_file.txt'  # Adjust as necessary
    output_file_path = 'sorted_output_file.txt'  # Adjust as necessary

    sort_file(input_file_path, output_file_path)

if __name__ == "__main__":
    main()
