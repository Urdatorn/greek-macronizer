import csv
from collections import defaultdict

def find_minimal_pairs(input_file_path, output_file_path):
    token_lines = defaultdict(list)

    # Read the file and collect lines by the first column
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        reader = csv.reader(input_file, delimiter='\t')
        for row in reader:
            # Ensure row has two columns
            if len(row) == 2:
                token_lines[row[0]].append(row)
            else:
                print(f"Skipping line due to incorrect format: {row}")

    # Find minimal pairs: tokens that appear more than once with different second columns
    minimal_pairs = []
    for token, lines in token_lines.items():
        if len(lines) > 1:
            unique_second_columns = set(line[1] for line in lines)
            if len(unique_second_columns) > 1:
                minimal_pairs.extend(lines)

    # Write minimal pairs to a new file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        writer = csv.writer(output_file, delimiter='\t')
        writer.writerows(minimal_pairs)

    print(f"Number of lines with minimal pairs: {len(minimal_pairs)}")
    if len(minimal_pairs) > 0:
        print(f"Minimal pairs have been written to {output_file_path}")

#def main():
#    input_file_path = "input.txt"  # Change this path as needed
#    output_file_path = "minimal_pairs.txt"
#    find_minimal_pairs(input_file_path, output_file_path)

#if __name__ == "__main__":
#    main()
        
find_minimal_pairs('crawl/macrons_wiktionary.txt', 'crawl/minimal_pairs.txt')
