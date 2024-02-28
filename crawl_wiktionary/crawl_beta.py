import beta_code
import argparse

def translate_to_beta_code(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file, \
             open(output_file_path, 'w', encoding='utf-8') as output_file:
            for line in input_file:
                # Remove any trailing newlines or spaces, translate to beta code, convert to uppercase, then write to output file
                translated_line = beta_code.greek_to_beta_code(line.strip()).upper() + '\n'
                output_file.write(translated_line)

        print(f"Processed content with Beta Code saved to: {output_file_path}")
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    # Argument parsing with default values for input and output
    parser = argparse.ArgumentParser(description='Translate Greek text to Beta Code and convert to uppercase for a file with one word per line.')
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', required=True, help='Output file path')
    args = parser.parse_args()

    # Call the function with the provided arguments
    translate_to_beta_code(args.input, args.output)

if __name__ == "__main__":
    main()