'''
Förbereda tokens som ska makroniseras i en dictionary
    1. Ta bort all punktuation, ev. förutom ' för elision (remove_punctuation.py) (möjligtvis skapas nya dubletter)
    2. Ta bort dubletter
    3. Ordna alfabetiskt
    4. Omvandla till BETA CODE (beta_code.py)
    5. Gör allt till gemener, i.e. ta bort alla '*' (möjligtvis skapas nya dubletter, så kolla dubletter igen)
    6. Ta bort alla rader vars TOKEN
        - ej innehåller α, ι, υ (A, I, U)
        - har cirkumflex på sin enda α, ι, υ (i.e. bara en A, I, U och denna följs av = innan nästa bokstav)
        - är properispomenon och inte har α, ι, υ på en tidigare stavelse än penultiman (behövs ej dictionary)
    7. Felaktig POS-analys:
        i. Om en TAG innehåller 'x' eller är kortare än nio tecken, flytta raden till lines_x.txt
        ii. Om ett LEMMA ej innehåller vokaler, flytta raden till lines_x.txt
'''

import argparse
import os
from utils import Colors

# all 7 token scripts 
import remove_punctuation
import remove_duplicates
import normalize
import alphabetize_unicode 

import handle_aberrant_lines
import handle_x_lines

def main(input_file_path, output_file_path, aberrant_lines_file_path, lines_with_x_file_path):
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    tokens_dir = os.path.join(current_script_dir, 'tokens')

    # Adjusting file paths to be relative to the script
    input_file_path = os.path.join(tokens_dir, input_file_path)
    output_file_path = os.path.join(tokens_dir, output_file_path)
    aberrant_lines_file_path = os.path.join(tokens_dir, aberrant_lines_file_path)
    lines_with_x_file_path = os.path.join(tokens_dir, lines_with_x_file_path)

    # Defining intermediate paths
    tokens_no_punct_path = os.path.join(tokens_dir, 'tokens_no_punct.txt')
    tokens_no_dup_path = os.path.join(tokens_dir, 'tokens_no_dup.txt')
    tokens_norm_path = os.path.join(tokens_dir, 'tokens_norm.txt')
    tokens_alph_path = os.path.join(tokens_dir, 'tokens_alph.txt')

    #tokens_beta_path = os.path.join(tokens_dir, 'tokens_beta.txt')
    #tokens_no_stars_path = os.path.join(tokens_dir, 'tokens_no_stars.txt')
    tokens_no_stars_no_dup_path = os.path.join(tokens_dir, 'tokens_no_stars_no_dup.txt')
    tokens_only_necessary_path = os.path.join(tokens_dir, 'tokens_only_necessary.txt')

    # Main flow
    print(f"{Colors.YELLOW}1. Removing punctuation and generating tokens_no_punct.txt{Colors.ENDC}")
    remove_punctuation.remove_punctuation_from_file(input_file_path, tokens_no_punct_path)
    
    print(f"{Colors.YELLOW}2. Removing duplicates and generating tokens_no_dup.txt{Colors.ENDC}")
    remove_duplicates.remove_duplicates(tokens_no_punct_path, tokens_no_dup_path)

    print(f"{Colors.YELLOW}3. Normalizing and generating tokens_norm.txt{Colors.ENDC}")
    normalize.normalize_columns(tokens_no_dup_path, tokens_norm_path)
    #normalize.normalize_columns('prepare_tokens/tokens/test_norm.txt', 'prepare_tokens/tokens/test_norm_changed.txt')

    print(f"{Colors.YELLOW}4. Sorting unicode alphabetically with pyuca and generating tokens_alph.txt{Colors.ENDC}")
    alphabetize_unicode.sort_greek_file(tokens_norm_path, tokens_alph_path)

    print(f"{Colors.YELLOW}5. Filtering unnecessary TOKENs to lines_aberrant.txt and generating tokens_only_necessary.txt{Colors.ENDC}")
    #handle_aberrant_lines.handle_aberrant_lines(tokens_alph_path, tokens_only_necessary_path, aberrant_lines_file_path)

    #print(f"{Colors.YELLOW}6. Sending lines with 'x' to lines_x.txt and generating tokens.txt{Colors.ENDC}")
    #handle_x_lines.handle_x_lines(tokens_only_necessary_path, output_file_path, lines_with_x_file_path)

    #print(f"{Colors.GREEN}Processing complete! tokens.txt generated.{Colors.ENDC}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a Greek text file through various cleanup and formatting steps.')
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', required=True, help='Final output file path (tokens.txt)')
    parser.add_argument('--aberrant', required=True, help='Output file path for aberrant lines (lines_aberrant.txt)')
    parser.add_argument('--xlines', required=True, help='Output file path for lines with x (lines_x.txt)')
    args = parser.parse_args()

    main(args.input, args.output, args.aberrant, args.xlines)
