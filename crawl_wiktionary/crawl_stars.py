import argparse

def remove_stars(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file, \
             open(output_file_path, 'w', encoding='utf-8') as output_file:
            for line in input_file:
                cleaned_line = line.replace('*', '')  # Remove all asterisks
                output_file.write(cleaned_line)
                
        print(f"All stars removed. Cleaned content saved to: {output_file_path}")
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Remove all '*' characters from a text file.")
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', required=True, help='Output file path')
    args = parser.parse_args()

    remove_stars(args.input, args.output)

if __name__ == "__main__":
    main()
