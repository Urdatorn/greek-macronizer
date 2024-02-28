import csv
import argparse

def count_non_unique_tokens(input_file_path):
    token_counts = {}
    non_unique_count = 0

    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            reader = csv.reader(input_file, delimiter='\t')
            for row in reader:
                if len(row) < 1:
                    continue  # Skip empty or malformed lines
                token = row[0]
                if token in token_counts:
                    token_counts[token] += 1
                else:
                    token_counts[token] = 1

        # Count tokens that appear more than once
        non_unique_count = sum(1 for count in token_counts.values() if count > 1)

        print(f"Number of non-unique tokens: {non_unique_count}")
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#def main():
#   parser = argparse.ArgumentParser(description='Count non-unique tokens in the first column of a three-column text file.')
#  parser.add_argument('--input', required=False, help='Input file path')
#    args = parser.parse_args()

#    count_non_unique_tokens(args.input)

#if __name__ == "__main__":
#    main()

count_non_unique_tokens('prepare_tokens/tokens/tokens.txt')