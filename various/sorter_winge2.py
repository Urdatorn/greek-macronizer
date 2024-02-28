import csv
import string
import re
import argparse
import os

class Colors:
    GREEN = '\033[1;32m'  # Green
    RED = '\033[1;31m'    # Red
    ENDC = '\033[0m'      # Reset to default color

# Unicode Constants
GREEK_ANO_TELEIA = '\u0387'
GREEK_QUESTION_MARK = '\u037E'
DAGGER = '\u2020'
EM_DASH = '\u2014'

# Unicode ranges for Greek characters
MONOTONIC_CHARS = set(range(0x370, 0x3FF + 1)) - {GREEK_ANO_TELEIA, GREEK_QUESTION_MARK}
POLYPHONIC_CHARS = set(range(0x1F00, 0x1FFF + 1))

# Merge both sets for a unified set of Greek characters
GREEK_CHARS = MONOTONIC_CHARS.union(POLYPHONIC_CHARS)

# Function to check if the string contains any Greek letters
def contains_greek(text):
    """
    Check if the provided text contains any Greek characters.
    
    The function checks if any character in the input text belongs to the predefined unified set of Greek characters. 
    
    Args:
        text (str): The text string to be checked for Greek characters.
    
    Returns:
        bool: True if the text contains any Greek characters, False otherwise.
    
    Example:
        sample_text = "Hello, κόσμος!"
        result = contains_greek(sample_text)
        print(result)  # Output: True
    """
    return any(char in GREEK_CHARS for char in map(ord, text))

# Function to remove surrounding punctuation and dagger from Greek characters
def remove_surrounding_punctuation(token_or_lemma):
    """
    Remove surrounding punctuation, including Greek-specific punctuation and dagger, from a token or lemma containing Greek characters.
    
    This function defines a pattern to match tokens or lemmas that may have surrounding punctuation (including common punctuation, Greek semicolon, Greek question mark, dagger, and em dash). It then removes this surrounding punctuation and returns the central part of the string, which contains the Greek characters.
    
    Args:
        token_or_lemma (str): The token or lemma from which surrounding punctuation and dagger are to be removed.
    
    Returns:
        str: The input string with surrounding punctuation and dagger removed, if present. If no surrounding punctuation or dagger is found, the original string is returned.
    
    Example:
        sample_token = "—Καλημέρα!—"
        result = remove_surrounding_punctuation(sample_token)
        print(result)  # Output: Καλημέρα
    """
    # Include common punctuation, Greek punctuation (Greek semicolon, Greek question mark, dagger), and the em dash
    punctuation = string.punctuation + GREEK_ANO_TELEIA + GREEK_QUESTION_MARK + DAGGER + EM_DASH
    
    # Pattern to match Greek characters possibly surrounded by punctuation/dagger/em dash
    pattern = r'^([' + re.escape(punctuation) + r']+)?(.*[\u0370-\u03ff\u1f00-\u1fff]+)([' + re.escape(punctuation) + r']+)?$'
    match = re.match(pattern, token_or_lemma)
    if match:
        return match.group(2)  # Return the part with Greek characters, excluding surrounding punctuation/dagger/em dash
    return token_or_lemma

# Paths to your input and output files
input_file_path = "tragedies_300595.txt"
output_file_path = "tokens.txt"
aberrant_file_path = "lines_aberrant.txt"
lines_with_x_file_path = "lines_x.txt"

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Process Greek text files.')
    parser.add_argument('--input', default='tragedies_300595.txt', help='Input file path (default: tragedies_300595.txt)')
    parser.add_argument('--output', default='tokens.txt', help='Output file path (default: tokens.txt)')
    parser.add_argument('--aberrant', default='lines_aberrant.txt', help='File path to write aberrant lines (default: lines_aberrant.txt)')
    parser.add_argument('--xlines', default='lines_x.txt', help='File path to write lines with x (default: lines_x.txt)')
    args = parser.parse_args()

    input_file_path = args.input
    output_file_path = args.output
    aberrant_file_path = args.aberrant
    lines_with_x_file_path = args.xlines

    # Initialize the counters and data collections
    total_input_lines = 0
    total_output_lines = 0
    total_duplicated_lines = 0
    data = []
    aberrant_lines = []
    lines_with_x = []

    '''
    Read the file and store the data
    1) remove_surrounding_punctuation fixes some lines
    2) Check i) # of delimiters and ii) whether there is any non-Greek in token or lemma. If fail => line sent to aberrant
    3) Check ii) Lines with tag length less than 9 characters or tag containing 'x' are added to lines_with_x
    ''' 
    # Read the file and store the data
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            # Check if the file is empty
            if os.stat(input_file_path).st_size == 0:
                print(f"{Colors.RED}Error: The input file is empty.{Colors.ENDC}")
                return
            
            reader = csv.reader(file, delimiter='\t')
            for row in reader:
                total_input_lines += 1
                modified_token = remove_surrounding_punctuation(row[0]) if len(row) > 0 else ""
                modified_lemma = remove_surrounding_punctuation(row[2]) if len(row) > 2 else ""
                
                # Check if the line should be added to lines_with_x first
                if len(row) == 3 and (contains_greek(modified_token) and contains_greek(modified_lemma)) and ('x' in row[1] or len(row[1]) < 9):
                    lines_with_x.append(row)
                # Check for the correct number of columns and Greek characters
                elif len(row) != 3 or not (contains_greek(modified_token) and contains_greek(modified_lemma)):
                    aberrant_lines.append(row)
                else:
                    data.append([modified_token, row[1], modified_lemma])
    
    except FileNotFoundError:
        print(f"{Colors.RED}Error: The file {input_file_path} was not found.{Colors.ENDC}")
        return
    except PermissionError:
        print(f"{Colors.RED}Error: Permission denied when accessing {input_file_path}.{Colors.ENDC}")
        return
    except Exception as e:
        print(f"{Colors.RED}An unexpected error occurred: {e}{Colors.ENDC}")
        return

    # Write aberrant lines to a separate file
    with open(aberrant_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        for row in aberrant_lines:
            writer.writerow(row)

    # Write lines with 'x' in the tag or with tag length less than 9 characters to a separate file
    with open(lines_with_x_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        for row in lines_with_x:
            writer.writerow(row)

    # Process the remaining data
    data_reordered = [(row[0], row[1], row[2]) for row in data]
    data_sorted = sorted(data_reordered, key=lambda x: (x[0], x[1]))
    seen = set()
    data_unique = []
    for row in data_sorted:
        row_tuple = tuple(row)
        if row_tuple not in seen:
            seen.add(row_tuple)
            data_unique.append(row)
        else:
            total_duplicated_lines += 1

    total_output_lines = len(data_unique)

    # Write the processed data to a new file
    with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        for row in data_unique:
            writer.writerow(row)

    # Print the required information
    print(f"{Colors.GREEN}Total number of input lines: {total_input_lines}{Colors.ENDC}")
    print(f"{Colors.GREEN}Total number of output lines (unique): {total_output_lines}{Colors.ENDC}")
    print(f"{Colors.RED}Total number of duplicated lines removed: {total_duplicated_lines}{Colors.ENDC}")
    print(f"{Colors.RED}Total number of aberrant lines: {len(aberrant_lines)}{Colors.ENDC}")
    print(f"{Colors.RED}Total number of x-lines: {len(lines_with_x)}{Colors.ENDC}")

    # Verify that the total number of lines processed matches the sum of output, aberrant, duplicated, and 'x' tag lines
    if total_input_lines != (total_output_lines + len(aberrant_lines) + total_duplicated_lines + len(lines_with_x)):
        print(f"{Colors.RED}Error: The number of input lines does not match the sum of output, aberrant, duplicated lines, and lines with 'x' in the tag!{Colors.ENDC}")
        print(f"{total_output_lines + len(aberrant_lines) + total_duplicated_lines + len(lines_with_x)}")
    else:
        print(f"{Colors.GREEN}Verification successful: All input lines are accounted for.{Colors.ENDC}")

if __name__ == "__main__":
    main()