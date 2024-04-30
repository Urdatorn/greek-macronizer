'''
Convert the raw ifthimos macrons, i.e.
    Ἀγαβάτας	n-s---mn-	Ἀγαβάτας	Αααᾱ
or
    ἀγαθάς	a-p---fa-	ἀγαθός	ααᾱ,
into a line with proper macrons, i.e.
    ἀγαθάς	a-p---fa-	ἀγαθός	_6

The raw ifthimos macrons only use the following characters:
    ΑαιυᾱᾹῑῙῡῩ
(with only 37 iotas and 44 hypsilons against 3104 alphas.)

Only 3183 lines have macrons from ifthimos.


'''


import csv
import re

from greek_accentuation.characters import length, base

from utils import only_bases, base_alphabet
from crawl_wiktionary.macrons_map import macrons_map


LONG = '̄'


### INITIAL AUXILIARIES


def strip_length_string(string):
    '''
    Strips the input string of all length diacritics using the macrons_map dictionary.
    >>> strip_length_string('ᾰᾸᾱᾹῐῘῑῙῠῨῡῩᾰ̓Ᾰ̓ᾰ̔Ᾰ̔ᾰ́ᾰ̀ᾱ̓Ᾱ̓ᾱ̔Ᾱ̔ᾱ́ᾱ̀ᾱͅῐ̓Ῐ̓ῐ̔Ῐ̔ῐ́ῐ̀ῐ̈ῑ̓Ῑ̓ῑ̔Ῑ̔ῑ́ῑ̈ῠ̓ῠ̔Ῠ̔ῠ́ῠ̀ῠ͂ῠ̈ῠ̒ῡ̔Ῡ̔ῡ́ῡ̈')
    >>> αΑαΑιΙιΙυΥυΥἀἈἁἉάὰἀἈἁἉάὰᾳἰἸἱἹίὶϊἰἸἱἹίϊὐὑὙύὺῦϋυ̒ὑὙύϋ
    '''
    for composite, replacement in macrons_map.items():
        string = string.replace(composite, replacement)
    return string


def process_word(word):
    '''
    Processes each word to identify vowel length markers and create a TSV format.
    '''
    
    modifications = []
    i = 1  # Initialize character position counter
    for char in word:
        if re.search(base_alphabet, base(char)):
            char_length = length(char)
            if char_length == LONG:
                modifications.append(f"_{i}")
            i += 1  # Only increment for non-length marking characters

    processed_word = strip_length_string(word)
    return processed_word, modifications


def placements_alpha(line):
    """
    Processes a given TSV line. If the base form of the fourth column contains the Greek letter alpha,
    process the word and return the 'placements' part of the result.

    >>placements_alpha('ἀγαθάς	a-p---fa-	ἀγαθός	ααᾱ')
    >>_3
    
    Parameters:
    - line (str): A string representing a row from a TSV file, expected to be tab-separated.

    Returns:
    - placements (str): The processed placements information if conditions are met, otherwise None.
    """
    try:
        # Split the line into columns using the tab delimiter
        columns = line.split('\t')
        
        # Ensure the line has at least four elements
        if len(columns) < 4:
            return None
        
        # Process the fourth column to remove diacritics
        base_text = only_bases(columns[3])
        
        # Check if the processed text contains 'α'
        if 'α' in base_text:
            # Assuming process_word returns a tuple or list and we need the second element
            result = process_word(columns[3])
            if result and len(result) > 1:
                placements = result[1]
                #print(placements)
                return placements
            
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def placements_iota(line):
    """
    Processes a given TSV line. If the base form of the fourth column contains the Greek letter alpha,
    process the word and return the 'placements' part of the result.

    >>placements_alpha('ἀγαθάς	a-p---fa-	ἀγαθός	ααᾱ')
    >>_3
    
    Parameters:
    - line (str): A string representing a row from a TSV file, expected to be tab-separated.

    Returns:
    - placements (str): The processed placements information if conditions are met, otherwise None.
    """
    try:
        # Split the line into columns using the tab delimiter
        columns = line.split('\t')
        
        # Ensure the line has at least four elements
        if len(columns) < 4:
            return None
        
        # Process the fourth column to remove diacritics
        base_text = only_bases(columns[3])
        
        # Check if the processed text contains 'α'
        if 'ι' in base_text:
            # Assuming process_word returns a tuple or list and we need the second element
            result = process_word(columns[3])
            if result and len(result) > 1:
                placements = result[1]
                return placements
            
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def placements_hypsilon(line):
    """
    Processes a given TSV line. If the base form of the fourth column contains the Greek letter alpha,
    process the word and return the 'placements' part of the result.

    >>placements_alpha('ἀγαθάς	a-p---fa-	ἀγαθός	ααᾱ')
    >>_3
    
    Parameters:
    - line (str): A string representing a row from a TSV file, expected to be tab-separated.

    Returns:
    - placements (str): The processed placements information if conditions are met, otherwise None.
    """
    try:
        # Split the line into columns using the tab delimiter
        columns = line.split('\t')
        
        # Ensure the line has at least four elements
        if len(columns) < 4:
            return None
        
        # Process the fourth column to remove diacritics
        base_text = only_bases(columns[3])
        
        # Check if the processed text contains 'α'
        if 'υ' in base_text:
            # Assuming process_word returns a tuple or list and we need the second element
            result = process_word(columns[3])
            if result and len(result) > 1:
                placements = result[1]
                return placements
            
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


### DIGIT FUNCTIONS


def extract_digit(result):
    """ Helper function to extract digit from the function return. """
    digits = re.findall(r'\d+', result)
    return int(digits[0]) if digits else None


def find_nth_character(base_text, character, n):
    """ Find the nth occurrence of a character in a string and return its position. """
    count = 0
    for index, char in enumerate(base_text):
        if char == character:
            count += 1
            if count == n:
                return index + 1  # returning 1-based index
    return None


### CONVERT MACRON FORMAT, TWO STEPS


def convert_placement(line):
    '''
    >>δῖναινεφέλας	n-p---fa-	δῖναινεφέλη	ῑᾱ
    >>{'α_position_1': 4, 'ι_position_1': 2}
    '''
    # Split the line assuming it's a single string of a TSV row
    columns = line.split('\t')
    
    if len(columns) < 4:
        return None

    # Apply base conversion to the first column (assuming the relevant text is in the first column)
    base_text = only_bases(columns[0])
    result_dict = {}

    # Define the specific character counters from the fourth column
    char_counts = {
        'α': columns[3].count('ᾱ') + columns[3].count('Ᾱ'),
        'ι': columns[3].count('ῑ') + columns[3].count('Ῑ'),
        'υ': columns[3].count('ῡ') + columns[3].count('Ῡ')
    }

    # Function mappings with separate lists to handle each type separately
    char_functions = {'α': placements_alpha, 'ι': placements_iota, 'υ': placements_hypsilon}

    # Iterate over each character type and process placements
    for char, func in char_functions.items():
        placements = func(line)
        if placements:
            # Calculate unique indices for the current character and respect the maximum allowed from the count
            unique_indices = set()  # To avoid duplicate processing for the same index
            for placement in placements:
                n = extract_digit(placement)
                if n and n not in unique_indices:
                    if len(unique_indices) < char_counts[char]:  # Check against the maximum allowed placements
                        position = find_nth_character(base_text, char, n)
                        if position is not None:
                            unique_indices.add(n)
                            # Save the position with a unique key
                            result_dict[f'{char}_position_{n}'] = position

    return result_dict


def format_placement_output(line):
    '''
    Takes a TSV line, applies convert_placement to get dictionary entries of character positions,
    and returns them in arithmetical order, prefixed with underscores.
    Example:
    >>line = 'δῖναινεφέλας\tn-p---fa-\tδῖναινεφέλη\tῑᾱ'
    >>format_placement_output(line)
    >>'_2_4'
    '''
    # Get the placement dictionary from convert_placement
    placement_dict = convert_placement(line)
    
    if not placement_dict:
        return ''
    
    # Sort the position numbers directly from the dictionary values
    sorted_positions = sorted(placement_dict.values())
    
    # Format the sorted position numbers as a single string with underscores
    formatted_output = '_' + '_'.join(map(str, sorted_positions))
    
    return formatted_output


def process_tsv_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8', newline='') as infile, \
         open(output_file_path, 'w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        # Read the header and write it directly to the output file
        header = next(reader)
        writer.writerow(header + [''])  # Ensure the header has five columns

        # Process each subsequent line
        for line in reader:
            if len(line) < 4:
                # Ensure the line has at least four columns to avoid index errors
                continue

            # Apply the placement formatting to the fourth column
            formatted_output = format_placement_output('\t'.join(line))
            line[3] = formatted_output

            # Ensure the line has exactly five columns
            while len(line) < 5:
                line.append('')

            # Write the modified line to the output file
            writer.writerow(line)





 
# unit tests
'''
print(f'Should be 5: {convert_placement('ἀγαθάς	a-p---fa-	ἀγαθός	ααᾱ')}')
print(f'Should be 3: {convert_placement('ἁψῖδα	n-s---fa-	ἁψῖδα	ῑ')}')
print(f'Should be 4 and 2: {convert_placement('δῖναινεφέλας	n-p---fa-	δῖναινεφέλη	ῑᾱ')}')
print(f'Should be 6: {convert_placement('δωματῖτιν	n-s---fa-	δωματῖτιν	ῑι')}')
print(f'Should be 1 and 3: {convert_placement('ᾄξας	n-p---fa-	ᾄξη	ᾱᾱ')}')
'''
'''
print(f'Should be 5: {format_placement_output('ἀγαθάς	a-p---fa-	ἀγαθός	ααᾱ')}')
print(f'Should be 3: {format_placement_output('ἁψῖδα	n-s---fa-	ἁψῖδα	ῑ')}')
print(f'Should be 4 and 2: {format_placement_output('δῖναινεφέλας	n-p---fa-	δῖναινεφέλη	ῑᾱ')}')
print(f'Should be 6: {format_placement_output('δωματῖτιν	n-s---fa-	δωματῖτιν	ῑι')}')
print(f'Should be 1 and 3: {format_placement_output('ᾄξας	n-p---fa-	ᾄξη	ᾱᾱ')}')
'''

# Example usage
input_file_path = 'macrons_ifthimos_raw_filter.tsv'
output_file_path = 'macrons_ifthimos.tsv'
process_tsv_file(input_file_path, output_file_path)
