import string
import unicodedata
import argparse

def remove_punctuation_from_file(input_file_path, output_file_path):
    # Define the specific Greek punctuation to remove
    GREEK_ANO_TELEIA = '\u0387'
    GREEK_QUESTION_MARK = '\u037E'
    DAGGER = '\u2020'
    EM_DASH = '\u2014'
    ELISION = '\u2019'
    
    # Include common punctuation and specific Greek punctuation
    punctuation = string.punctuation + GREEK_ANO_TELEIA + GREEK_QUESTION_MARK + DAGGER + EM_DASH
    
    # Create a translation table: maps each character to None (for removal)
    # Exclude the ELISION sign from removal
    remove_punct_map = dict.fromkeys(map(ord, punctuation), None)
    remove_punct_map[ord(ELISION)] = ELISION  # Keep the ELISION sign

    # Counters for punctuation removed
    punctuation_removed_count = 0

    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file, \
             open(output_file_path, 'w', encoding='utf-8') as output_file:
            for line in input_file:
                # Split the line into three parts
                parts = line.strip().split('\t')
                
                # Check if the line has exactly three parts
                if len(parts) == 3:
                    # Count and remove punctuation from the first and third parts
                    for i in [0, 2]:
                        original_len = len(parts[i])
                        parts[i] = parts[i].translate(remove_punct_map)
                        parts[i] = unicodedata.normalize('NFC', parts[i])  # Normalize
                        punctuation_removed_count += original_len - len(parts[i])
                    
                    # Write the processed parts back to the output file
                    output_file.write('\t'.join(parts) + '\n')
                #else:
                    #print(f"Skipping line due to incorrect format: {line.strip()}")

        print(f"Processed content saved to: {output_file_path}")
        print(f"Total punctuation characters removed: {punctuation_removed_count}")
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    # Argument parsing with default values for input and output
    parser = argparse.ArgumentParser(description='Remove punctuation from specific fields in a text file.')
    parser.add_argument('--input', default='tokens/tokens_no_duplicates.txt', help='Input file path (default: tragedies_300595.txt)')
    parser.add_argument('--output', default='tokens/tokens_no_punct.txt', help='Output file path (default: tokens2.txt)')
    args = parser.parse_args()

    # Call the function with the provided arguments
    remove_punctuation_from_file(args.input, args.output)

if __name__ == "__main__":
    main()
