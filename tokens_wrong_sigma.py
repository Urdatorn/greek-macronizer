import re
import csv
from tqdm import tqdm
from utils import Colors, all_consonants, with_spiritus

# Define the patterns to match final sigma at non-final positions
wrong_final_sigma = r'ς(?=.)'
wrong_final_sigma_before_consonant = fr'ς(?={all_consonants})'
wrong_final_sigma_before_spiritus = fr'ς(?={with_spiritus})'

input_file_path = 'prepare_tokens/tokens/tokens.txt'
output_file_path = 'tokens_wrong_sigma.txt'

# Initialize counters for lines matching each pattern
count_wrong_final_sigma = 0
count_wrong_sigma_before_consonant = 0
count_wrong_sigma_before_spiritus = 0

with open(input_file_path, 'r', encoding='utf-8') as infile, \
     open(output_file_path, 'w', encoding='utf-8') as outfile:
    for line in tqdm(infile, desc="Scanning for incorrect sigma usage"):
        token = line.split('\t')[0]
        if re.search(wrong_final_sigma, token):
            count_wrong_final_sigma += 1
            outfile.write(line)
        if re.search(wrong_final_sigma_before_consonant, token):
            count_wrong_sigma_before_consonant += 1
        if re.search(wrong_final_sigma_before_spiritus, token):
            count_wrong_sigma_before_spiritus += 1

print(f"{Colors.GREEN}Total tokens with ς at non-final positions: {count_wrong_final_sigma}{Colors.ENDC}")
print(f"{Colors.GREEN}Total tokens with ς before a consonant: {count_wrong_sigma_before_consonant}{Colors.ENDC}")
print(f"{Colors.GREEN}Total tokens with ς before spiritus: {count_wrong_sigma_before_spiritus}{Colors.ENDC}")
