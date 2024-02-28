import csv
import argparse

# Mapping of Beta Code letters to their sorting order. no 'J' or 'V'
BETA_CODE_ORDER = {
    'A': 1, 'B': 2, 'G': 3, 'D': 4, 'E': 5, 'Z': 6, 'H': 7, 'Q': 8,
    'I': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'C': 14, 'O': 15,
    'P': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'F': 21, 'X': 22,
    'Y': 23, 'W': 24
}

def beta_code_sort_key(word):
    """
    Returns a list of numbers representing the sorting order of each character in a word,
    based on the Beta Code order. Ignores characters not in BETA_CODE_ORDER.
    """
    # Filter to include only characters present in BETA_CODE_ORDER, converting to uppercase to match the dictionary keys
    filtered_chars = [char.upper() for char in word if char.upper() in BETA_CODE_ORDER]
    return [BETA_CODE_ORDER.get(char, 0) for char in filtered_chars]

def sort_dictionary(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file, \
             open(output_file_path, 'w', encoding='utf-8') as output_file:
            rows = list(csv.reader(input_file, delimiter='\t'))
            
            # Sort the rows first by LEMMA (3rd column) then by TOKEN (1st column)
            sorted_rows = sorted(rows, key=lambda row: (beta_code_sort_key(row[2]), beta_code_sort_key(row[0])))
            
            writer = csv.writer(output_file, delimiter='\t')
            writer.writerows(sorted_rows)
            
        print(f"Sorted content saved to: {output_file_path}")
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Sort a 3-column dictionary text file by LEMMA and TOKEN in Beta Code alphabetical order, ignoring non-Beta Code characters.')
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', required=True, help='Output file path')
    args = parser.parse_args()

    sort_dictionary(args.input, args.output)

if __name__ == "__main__":
    main()
