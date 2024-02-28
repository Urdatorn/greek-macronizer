import csv
import beta_code
import argparse

def translate_to_beta_code(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file, \
             open(output_file_path, 'w', encoding='utf-8') as output_file:
            reader = csv.reader(input_file, delimiter='\t')
            writer = csv.writer(output_file, delimiter='\t')
            
            for row in reader:
                if len(row) == 3:
                    # Translate the first and third fields using beta_code and convert to uppercase
                    row[0] = beta_code.greek_to_beta_code(row[0]).upper()
                    row[2] = beta_code.greek_to_beta_code(row[2]).upper()
                    
                    # Write the translated and uppercased row back to the output file
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
    parser = argparse.ArgumentParser(description='Translate Greek text to Beta Code and convert to uppercase in specific fields of a text file.')
    parser.add_argument('--input', default='tokens/tokens_no_punct.txt', help='Input file path (default: tokens2.txt)')
    parser.add_argument('--output', default='tokens/tokens_no_punct_beta.txt', help='Output file path (default: tokens_beta.txt)')
    args = parser.parse_args()

    # Call the function with the provided arguments
    translate_to_beta_code(args.input, args.output)

if __name__ == "__main__":
    main()
