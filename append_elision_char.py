'''
stop words
οὐκ
ἐκ
'''

from utils import Colors

def append_elision_char(input_file_path, output_file_path):
    elision_char = '\u2019'  # RIGHT SINGLE QUOTATION MARK (’)
    incorrect_final_consonants = ('β', 'γ', 'δ', 'ζ', 'θ', 'κ', 'λ', 'μ', 'π', 'σ', 'τ', 'φ', 'χ')
    elision_appended_count = 0

    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
         open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in input_file:
            columns = line.strip().split('\t')
            if columns and columns[2] != 'ἐκ' and columns[0] != 'ἐκ' and columns[2] != 'οὐ' and columns[0] != 'οὐκ' and columns[0] != 'οὐχ' and columns[2] != 'οὔ' and columns[0] != 'Οὔκ' and any(columns[0].endswith(consonant) for consonant in incorrect_final_consonants):
                columns[0] += elision_char  # Append the elision character to the end of the first column
                elision_appended_count += 1
            output_file.write('\t'.join(columns) + '\n')

    print(f"{Colors.GREEN}Elision characters appended: {elision_appended_count}{Colors.ENDC}")

# Example usage
input_file_path = 'tokens_elided.txt'
output_file_path = 'tokens_elided_fixed.txt'
append_elision_char(input_file_path, output_file_path)
