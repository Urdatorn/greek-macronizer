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

# Append the root folder to sys.path to be able to import from /utils.py
# Assuming the script is in a subfolder one level deep from the root
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# continue with the imports
import argparse
from utils import Colors
from stats import write_stats

# all token scripts 
import remove_punctuation
import remove_duplicates
import remove_lines_few_columns
import normalize
import supplement_barytones
import alphabetize_unicode 
import filter_dichrona
import handle_x_lines
import remove_double_accents
import remove_no_spiritus

def print_ascii_art():
    cyan = Colors.CYAN
    endc = Colors.ENDC

    print(cyan + " _        _                   _        _   " + endc)
    print(cyan + "| |_ ___ | | _____ _ __  ___ | |___  _| |_ " + endc)
    print(cyan + "| __/ _ \\| |/ / _ \\ '_ \\/ __|| __\\ \\/ / __|" + endc)
    print(cyan + "| || (_) |   <  __/ | | \\__ \\| |_ >  <| |_ " + endc)
    print(cyan + " \\__\\___/|_|\\_\\___|_| |_|___(_)__/_/\\_\\__|" + endc)


def main(input_file_path, output_file_path, aberrant_lines_file_path, lines_with_x_file_path):
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    tokens_dir = os.path.join(current_script_dir, 'tokens')

    # Defining relative paths: in and out
    input_file_path = os.path.join(tokens_dir, input_file_path)
    output_file_path = os.path.join(tokens_dir, output_file_path)
    aberrant_lines_file_path = os.path.join(tokens_dir, aberrant_lines_file_path)
    lines_with_x_file_path = os.path.join(tokens_dir, lines_with_x_file_path)

    # Defining relative paths: intermediate
    tokens_no_punct_path = os.path.join(tokens_dir, 'tokens_no_punct.txt')
    tokens_no_dup_path = os.path.join(tokens_dir, 'tokens_no_dup.txt')
    tokens_three_columns_path = os.path.join(tokens_dir, 'tokens_three_columns.txt')
    tokens_norm_path = os.path.join(tokens_dir, 'tokens_norm.txt')
    tokens_oxytone_path = os.path.join(tokens_dir, 'tokens_oxytone.txt')
    tokens_alph_path = os.path.join(tokens_dir, 'tokens_alph.txt')
    tokens_only_necessary_path = os.path.join(tokens_dir, 'tokens_dichrona.txt')
    tokens_no_x_path = os.path.join(tokens_dir, 'tokens_no_x.txt')
    tokens_no_double_accents_path = os.path.join(tokens_dir, 'tokens_no_double_accents.txt')

    # Main flow
    print_ascii_art()
    print(f"{Colors.CYAN} Starting to prepare tokens.txt!{Colors.ENDC}")
    print(f"{Colors.CYAN} Input: 300595 lines of all tokens in Aeschylus with POS analysis and lemmatization{Colors.ENDC}")

    print(f"{Colors.YELLOW}1. Removing punctuation and generating tokens_no_punct.txt{Colors.ENDC}")
    remove_punctuation.process_file(input_file_path, tokens_no_punct_path)
    
    print(f"{Colors.YELLOW}2. Removing duplicates and generating tokens_no_dup.txt{Colors.ENDC}")
    remove_duplicates.remove_duplicates(tokens_no_punct_path, tokens_no_dup_path)

    print(f"{Colors.YELLOW}3. Removing lines with too few columns (or first column empty of Greek) and generating tokens_three_columns.txt{Colors.ENDC}")
    remove_lines_few_columns.remove_lines_few_columns(tokens_no_dup_path, tokens_three_columns_path)

    print(f"{Colors.YELLOW}4. Normalizing and generating tokens_norm.txt{Colors.ENDC}")
    normalize.normalize_columns(tokens_three_columns_path, tokens_norm_path)

    print(f"{Colors.YELLOW}5. Adding oxytone versions of every barytone token and generating tokens_oxytone.txt{Colors.ENDC}")
    supplement_barytones.process_tokens_file(tokens_norm_path, tokens_oxytone_path)

    print(f"{Colors.YELLOW}5. Sorting unicode alphabetically with pyuca and generating tokens_alph.txt{Colors.ENDC}")
    alphabetize_unicode.sort_greek_file(tokens_oxytone_path, tokens_alph_path)

    print(f"{Colors.YELLOW}6. Filtering truly undecided dichrona to tokens_dichrona.txt and sending the rest to lines_filtered_out.txt{Colors.ENDC}")
    filter_dichrona.main(tokens_alph_path, tokens_only_necessary_path, aberrant_lines_file_path)

    print(f"{Colors.YELLOW}7. Sending lines with 'x' to lines_x.txt and generating tokens.txt{Colors.ENDC}")
    handle_x_lines.handle_x_lines(tokens_only_necessary_path, tokens_no_x_path, lines_with_x_file_path)

    print(f"{Colors.YELLOW}8. Removing the last accent of words with two accents{Colors.ENDC}")
    remove_double_accents.process_file(tokens_no_x_path, tokens_no_double_accents_path)

    print(f"{Colors.YELLOW}9. Removing words lacking obligatory spīritūs{Colors.ENDC}")
    remove_no_spiritus.process_tsv_file(tokens_no_double_accents_path, output_file_path)

    print(f"{Colors.CYAN}Processing complete! tokens.txt generated.{Colors.ENDC}")
    print(f"{Colors.CYAN}Saving statistics to stats.txt.{Colors.ENDC}")
    write_stats([output_file_path, lines_with_x_file_path, aberrant_lines_file_path], 'prepare_tokens/tokens/stats.txt')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a Greek text file through various cleanup and formatting steps.')
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', required=True, help='Final output file path (tokens.txt)')
    parser.add_argument('--aberrant', required=True, help='Output file path for aberrant lines (lines_aberrant.txt)')
    parser.add_argument('--xlines', required=True, help='Output file path for lines with x (lines_x.txt)')
    args = parser.parse_args()

    main(args.input, args.output, args.aberrant, args.xlines)
