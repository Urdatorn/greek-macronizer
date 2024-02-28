import csv
import argparse

def count_unique_tokens(file1_path, file2_path):
    # Load the first column of file 1 into a set for unique tokens
    tokens_file1 = set()
    with open(file1_path, 'r', encoding='utf-8') as file1:
        reader = csv.reader(file1, delimiter='\t')
        for row in reader:
            if row:  # Check if row is not empty
                tokens_file1.add(row[0])

    # Load the first column of file 2 into a set
    tokens_file2 = set()
    with open(file2_path, 'r', encoding='utf-8') as file2:
        reader = csv.reader(file2, delimiter='\t')
        for row in reader:
            if row:  # Check if row is not empty
                tokens_file2.add(row[0])

    # Find tokens in file 1 that do not appear in file 2
    unique_tokens = tokens_file1.difference(tokens_file2)

    # Print the count of unique tokens
    print(f"Number of unique tokens in {file1_path} not found in {file2_path}: {len(unique_tokens)}")

#def main():
#    parser = argparse.ArgumentParser(description="Compare the first columns of two files and count how many tokens in the first file do not appear in the first column of the second file.")
#    parser.add_argument('--file1', required=True, help="Path to the first input file")
#    parser.add_argument('--file2', required=True, help="Path to the second input file")
#    args = parser.parse_args()

#    count_unique_tokens(args.file1, args.file2)

#if __name__ == "__main__":
#    main()

count_unique_tokens('prepare_tokens/tokens/tokens.txt', 'crawl/macrons_wiktionary.txt')