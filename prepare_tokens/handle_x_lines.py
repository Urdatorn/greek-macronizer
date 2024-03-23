# Append the root folder to sys.path to be able to import from /utils.py
# Assuming your script is in a subfolder one level deep from the root
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
import argparse
import os

from utils import Colors, DICHRONA

def handle_x_lines(input_file_path, output_file_path, lines_with_x_file_path):
    total_input_lines = 0
    lines_with_x = []
    non_x_lines = []  # To hold lines that do not meet the criteria for x_lines
    
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='\t')
            for row in reader:
                total_input_lines += 1

                # Unpack the row for clarity
                token, tag, lemma = row

                # Check for the conditions that would move the line to lines_with_x.txt
                if 'x' in tag or 'X' in tag or len(tag) < 9:
                    lines_with_x.append(row)
                else:
                    non_x_lines.append(row)
    
    except FileNotFoundError:
        print(f"{Colors.RED}Error: The file {input_file_path} was not found.{Colors.ENDC}")
        return
    except PermissionError:
        print(f"{Colors.RED}Error: Permission denied when accessing {input_file_path}.{Colors.ENDC}")
        return
    except Exception as e:
        print(f"{Colors.RED}An unexpected error occurred: {e}{Colors.ENDC}")
        return

    # Write lines with 'x' in the tag or with tag length less than 9 characters, or lemmas without vowels, to lines_with_x.txt
    with open(lines_with_x_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerows(lines_with_x)

    # Write the remaining lines to the output file
    with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerows(non_x_lines)

    # Print summary information
    print(f"{Colors.GREEN}Total number of input lines: {total_input_lines}{Colors.ENDC}")
    print(f"{Colors.RED}Total number of x-lines: {len(lines_with_x)}{Colors.ENDC}")
    print(f"{Colors.GREEN}x-lines saved to: {lines_with_x_file_path}{Colors.ENDC}")
    print(f"{Colors.GREEN}Remaining lines saved to: {output_file_path}{Colors.ENDC}")

if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description='Separate lines based on specific criteria from a 3-column text file.')
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', required=True, help='Output file path for non-x lines')
    parser.add_argument('--xlines', required=True, help='File path to write lines with x')
    args = parser.parse_args()

    # Call handle_x_lines with the provided arguments
    handle_x_lines(args.input, args.output, args.xlines)
