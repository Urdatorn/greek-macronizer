import argparse
from greek_accentuation.characters import length, strip_length

SHORT = '̆'
LONG = '̄'

def process_word(word, length_count):
    processed_word = ""
    modifications = []
    for i, char in enumerate(word, start=1):  # Start counting from 1 for human readability
        char_length = length(char)
        if char_length == LONG:
            processed_word += strip_length(char)
            modifications.append(f"_{i}")
            length_count['long'] += 1
        elif char_length == SHORT:
            processed_word += strip_length(char)
            modifications.append(f"^{i}")
            length_count['short'] += 1
        else:
            processed_word += char
    return processed_word, modifications

def process_file(input_file_path, output_file_path):
    length_count = {'long': 0, 'short': 0}
    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file, \
             open(output_file_path, 'w', encoding='utf-8') as output_file:
            for line in input_file:
                parts = line.strip().split('\t')
                processed_word, modifications = process_word(parts[0], length_count)
                # Update the tag column with modifications
                if len(parts) > 1:
                    parts[1] += ''.join(modifications)
                else:
                    parts.append(''.join(modifications))
                parts[0] = processed_word
                output_file.write('\t'.join(parts) + '\n')
        print(f"Processing complete. Output saved to: {output_file_path}")
        print(f"Total macrons (long) stripped: {length_count['long']}")
        print(f"Total breves (short) stripped: {length_count['short']}")
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Modify polytonic Greek words to handle macrons and breves, appending markers and their positions to the tag column.')
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', required=True, help='Output file path')
    args = parser.parse_args()

    process_file(args.input, args.output)

if __name__ == "__main__":
    main()
