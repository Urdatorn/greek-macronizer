import re

def normalize_delimiters(input_file_path, output_file_path):
    # Regular expression to match sequences of spaces and/or tabs
    spaces_tabs_regex = re.compile(r'[ \t]+')
    
    lines_processed = 0
    replacements_made = 0

    with open(input_file_path, 'r', encoding='utf-8') as infile, \
         open(output_file_path, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            lines_processed += 1
            # Find all occurrences of the pattern
            matches = spaces_tabs_regex.findall(line)
            if matches:
                replacements_made += len(matches)
                # Replace sequences of spaces and/or tabs with a single tab
                line = spaces_tabs_regex.sub('\t', line)
            outfile.write(line)
    
    return lines_processed, replacements_made

# Paths to your input and output files
input_file_path = 'prepare_tokens/tokens/tokens_alph.txt'
output_file_path = 'prepare_tokens/tokens/tokens_alph_delimiters.txt'

lines_processed, replacements_made = normalize_delimiters(input_file_path, output_file_path)

print(f"Total lines processed: {lines_processed}")
print(f"Total replacements made: {replacements_made}")
