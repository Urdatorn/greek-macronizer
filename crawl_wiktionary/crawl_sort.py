import argparse

# Mapping of Beta Code letters to their sorting order. no 'J' or 'V'
BETA_CODE_ORDER = {
    'A': 1, 'B': 2, 'G': 3, 'D': 4, 'E': 5, 'Z': 6, 'H': 7, 'Q': 8,
    'I': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'C': 14, 'O': 15,
    'P': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'F': 21, 'X': 22,
    'Y': 23, 'W': 24
}

def beta_code_sort_key(word):
    """
    Returns a list of numbers representing the sorting order of each character in a word,
    based on the Beta Code order. Ignores characters not in BETA_CODE_ORDER.
    """
    # Filter to include only characters present in BETA_CODE_ORDER, converting to uppercase to match the dictionary keys
    filtered_chars = [char.upper() for char in word if char.upper() in BETA_CODE_ORDER]
    return [BETA_CODE_ORDER.get(char, 0) for char in filtered_chars]

# Define the order for punctuation
PUNCTUATION_ORDER = ")/=\\+|"

def enhanced_sort_key(word):
    # First, sort by Beta Code alphabetical order
    primary_key = beta_code_sort_key(word.strip())

    # Then, sort by the specified punctuation order if there are ties
    punctuation_key = [PUNCTUATION_ORDER.index(char) if char in PUNCTUATION_ORDER else len(PUNCTUATION_ORDER) for char in word]
    
    return primary_key, punctuation_key

def sort_file(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            words = input_file.readlines()
        
        # Sort words using the enhanced_sort_key
        sorted_words = sorted(words, key=enhanced_sort_key)
        
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for word in sorted_words:
                output_file.write(word)
                
        print(f"Sorted content saved to: {output_file_path}")
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Sort a text file of words in Beta Code alphabetical order, considering specified punctuation order for ties.')
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', required=True, help='Output file path for sorted words')
    args = parser.parse_args()

    sort_file(args.input, args.output)

if __name__ == "__main__":
    main()
