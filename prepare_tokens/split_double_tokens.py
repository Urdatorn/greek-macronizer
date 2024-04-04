'''
Manually fixed buggy lines identified here:

φθονήσῃςεὐγμάτων	n-p---ng-	φθονήσῃςεὐγμάτων
=>
φθονήσῃς	v--------	φθονέω
εὐγμάτων	n-p---ng-	εὖγμα

δύςοιστον	m--------	δύς 
=> 
δύσοιστον	a-s---fa-	δύσοιστος

φλαύροιςεἴτ’	a-p---md-	φλαύροιςεἴτ
=>
φλαύροις	a-p---md-	φλαῦρος
εἴτ’	d--------	εἶτα
'''

import re
import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tqdm import tqdm
from utils import Colors, with_spiritus


log_file_path = 'prepare_tokens/tokens.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(message)s')

all_consonants = r'[ΒΓΔΖΘΚΛΜΝΞΠΡΣΤΦΧΨβγδζθκλμνξπρστφχψ]' # except final sigma

# Define the patterns to match final sigma at non-final positions
wrong_final_sigma = r'ς(?!\u2019)(?=.)' # a negative lookahead assertion (?!) followed by a positive (?=)
wrong_final_sigma_before_consonant = fr'ς(?={all_consonants})'
wrong_final_sigma_before_spiritus = fr'ς(?={with_spiritus})'


def split_tokens_with_wrong_sigma(input_file_path, output_file_path):
    # Initialize counters for lines matching each pattern
    count_wrong_final_sigma = 0
    count_lines_split = 0
    count_buggy_lines_printed = 0

    logging.info(f"### split_double_tokens ###")

    with open(input_file_path, 'r', encoding='utf-8') as infile, \
         open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in tqdm(infile, desc="Scanning for incorrect sigma usage"):
            columns = line.strip().split('\t')
            token = columns[0]
            
            # Check for tokens that match specific patterns and log accordingly
            if re.search(wrong_final_sigma_before_consonant, token):
                logging.info(f"Final sigma before consonant: {line.strip()}")
                count_lines_split += 1
            if re.search(wrong_final_sigma_before_spiritus, token):
                logging.info(f"Final sigma before spiritus: {line.strip()}")
                count_lines_split += 1
            
            # Check for tokens that need splitting
            if re.search(wrong_final_sigma_before_consonant, token) or re.search(wrong_final_sigma_before_spiritus, token):
                match = re.search(r'(ς(?=.)[^ς]*)', token)
                if match:
                    split_point = match.start(1) + 1
                    part1 = token[:split_point]
                    part2 = token[split_point:]
                    outfile.write("\t".join([part1, columns[1], part1]) + "\n")
                    outfile.write("\t".join([part2, columns[1], part2]) + "\n")
                    logging.info(f"Split lines: {[part1, columns[1], part1]}, {[part2, columns[1], part2]}")
            elif re.search(wrong_final_sigma, token):
                logging.info(f"Buggy line: {line.strip()}")
                count_buggy_lines_printed += 1
            else:
                # Write the line unchanged if it doesn't match any pattern
                outfile.write(line)

    print(f"{Colors.GREEN}Lines split: {count_lines_split}{Colors.ENDC}")
    print(f"{Colors.RED}Buggy lines printed: {count_buggy_lines_printed}{Colors.ENDC}")

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    input_file_path = 'prepare_tokens/tokens/tokens.txt'
    output_file_path = 'tokens_wrong_sigma.txt'
    split_tokens_with_wrong_sigma(input_file_path, output_file_path)