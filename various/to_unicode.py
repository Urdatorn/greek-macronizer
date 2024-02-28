import csv
from beta_code import beta_code_to_greek
import argparse

def translate_to_beta_code(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file, \
             open(output_file_path, 'w', encoding='utf-8') as output_file:
            reader = csv.reader(input_file, delimiter='\t')
            writer = csv.writer(output_file, delimiter='\t')
            
            for row in reader:
                if len(row) == 3:
                    # Translate the first and third fields
                    row[0] = beta_code_to_greek(row[0])
                    row[2] = beta_code_to_greek(row[2])
                    
                    # Write the translated row back to the output file
                    writer.writerow(row)
                else:
                    print(f"Skipping line due to incorrect format: {row}")

        print(f"Processed content with Beta Code saved to: {output_file_path}")
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    # Argument parsing with default values for input and output
    parser = argparse.ArgumentParser(description='Translate Beta Code to unicode in specific fields of a text file.')
    parser.add_argument('--input', default='tokens/tokens_no_punct_beta.txt', help='Input file path (default: tokens/tokens_no_punct_beta.txt)')
    parser.add_argument('--output', default='tokens/tokens_no_punct_compare.txt', help='Output file path (default: tokens/tokens_no_punct_compare.txt, overwrites input)')
    args = parser.parse_args()

    # Call the function with the provided arguments
    translate_to_beta_code(args.input, args.output)

if __name__ == "__main__":
    main()
