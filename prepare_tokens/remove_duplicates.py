import csv
from utils import Colors
import argparse

def remove_duplicates(input_file_path, output_file_path):
    total_input_lines = 0
    total_output_lines = 0
    total_duplicated_lines = 0
    data = set()  # Use a set to automatically handle duplicates
    
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='\t')
            for row in reader:
                total_input_lines += 1
                
                # Convert row to tuple for immutability (required for set operations)
                row_tuple = tuple(row)
                
                if row_tuple in data:
                    total_duplicated_lines += 1
                else:
                    data.add(row_tuple)

    except FileNotFoundError:
        print(f"{Colors.RED}Error: The file {input_file_path} was not found.{Colors.ENDC}")
        return
    except PermissionError:
        print(f"{Colors.RED}Error: Permission denied when accessing {input_file_path}.{Colors.ENDC}")
        return
    except Exception as e:
        print(f"{Colors.RED}An unexpected error occurred: {e}{Colors.ENDC}")
        return

    total_output_lines = len(data)

    # Write the processed data to a new file
    with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        for row in data:
            writer.writerow(row)

    # Print summary information
    print(f"{Colors.GREEN}File processed and saved as: {output_file_path}{Colors.ENDC}")
    print(f"{Colors.GREEN}Total number of input lines: {total_input_lines}{Colors.ENDC}")
    print(f"{Colors.GREEN}Total number of output lines (unique): {total_output_lines}{Colors.ENDC}")
    print(f"{Colors.RED}Total number of duplicated lines removed: {total_duplicated_lines}{Colors.ENDC}")

    # Verify that the total number of lines processed matches the sum of unique and duplicated lines
    if total_input_lines != (total_output_lines + total_duplicated_lines):
        print(f"{Colors.RED}Error: The total number of input lines does not match the sum of output and duplicated lines!{Colors.ENDC}")
    else:
        print(f"{Colors.GREEN}Verification successful: All input lines are accounted for.{Colors.ENDC}")

if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description='Remove duplicate lines from a Greek text file.')
    parser.add_argument('--input', default='tokens/tragedies_300595.txt', help='Input file path')
    parser.add_argument('--output', default='tokens/tokens_no_duplicates.txt', help='Output file path')
    args = parser.parse_args()

    # Call remove_duplicates with the provided arguments
    remove_duplicates(args.input, args.output)
