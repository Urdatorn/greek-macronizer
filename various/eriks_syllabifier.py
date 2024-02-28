# step 2 in the scansion tool: divides the greek into syllables (except for double consonants and muta-cum-liquida, which I deal with later instead). Do not edit the resulting JSON manually!
import json
import re

# Global definition of regex patterns for different categories
patterns = {
    'diphth_y': r'(α|ε|η|ο)(ὐ|ὔ|υ|ὑ|ύ|ὖ|ῦ|ὕ|ὗ|ὺ|ὒ|ὓ)',
    'diphth_i': r'(α|ε|ο|υ)(ἰ|ί|ι|ῖ|ἴ|ἶ|ἵ|ἱ|ἷ|ὶ|ἲ|ἳ)',
    'adscr_i': r'(α|η|ω|ἀ|ἠ|ὠ|ἁ|ἡ|ὡ|ά|ή|ώ|ὰ|ὴ|ὼ|ᾶ|ῆ|ῶ|ὤ|ὥ|ὢ|ὣ|ἄ|ἅ|ἂ|ἃ|ἤ|ἥ|ἣ|ἢ|ἦ|ἧ|ἆ|ἇ|ὧ|ὦ)(ι)',
    'subscr_i': r'(ᾄ|ᾂ|ᾆ|ᾀ|ᾅ|ᾃ|ᾇ|ᾁ|ᾴ|ᾲ|ᾶ|ᾷ|ᾳ|ᾔ|ᾒ|ᾖ|ᾐ|ᾕ|ᾓ|ᾗ|ᾑ|ῄ|ῂ|ῃ|ᾤ|ᾢ|ᾦ|ᾠ|ᾥ|ᾣ|ᾧ|ᾡ|ῴ|ῲ|ῷ|ῳ|ῇ)',
    'stops': r'[πκτβδγφχθ]',
    'liquids': r'[ρλῥ]',
    'nasals': r'[μν]',
    'double_cons': r'[ζξψ]',
    'sibilants': r'[σς]',
    'vowels': r'[αεηιυωοἀἁἐἑἰἱὀὁἠἡὐὑὠὡάὰέὲήὴόὸίὶὺύώὼἄἅἔἕὄὅὂὃἤἥἴἵὔὕὤὥἂἃἒἓἢἣἲἳὒὓὢὣᾶῆῖῦῶἇἆἦἧἶἷὖὗὦὧϋϊΐῒϋῢΰῗῧ]'
}

def is_vowel(element):
    return any(re.match(patterns[vowel_type], element) for vowel_type in ['vowels', 'diphth_y', 'diphth_i', 'adscr_i', 'subscr_i'])

def is_consonant(element):
    return any(re.match(patterns[consonant_type], element) for consonant_type in ['stops', 'liquids', 'nasals', 'double_cons', 'sibilants'])

def syllabify(divided_text):
    elements = divided_text.split()
    syllables = []
    current_syllable = ''

    for element in elements:
        if is_vowel(element):
            # If there's already content in the current syllable, add it as a complete syllable
            if current_syllable:
                syllables.append(current_syllable)
                current_syllable = ''

            # Add the vowel to the current (now empty) syllable
            current_syllable = element
        else:
            # Add non-vowel elements to the current syllable
            current_syllable += element

    # Add the final syllable if it exists
    if current_syllable:
        syllables.append(current_syllable)

    return syllables

def reshuffle_consonants(syllables):
    reshuffled_syllables = []
    carry_over = ''

    for i in range(len(syllables)):
        syllable = syllables[i]

        # Handle start of line cases
        if i == 0 and not is_vowel(syllable[0]):
            vowel_index = next((index for index, char in enumerate(syllable) if is_vowel(char)), len(syllable))
            reshuffled_syllables.append(syllable[:vowel_index])
            carry_over = syllable[vowel_index:]
            continue

        # Prepend carry_over if present
        syllable = carry_over + syllable
        carry_over = ''

        # Simple and Complex case handling
        if i < len(syllables) - 1 and is_consonant(syllable[-1]):
            next_syllable = syllables[i + 1]
            if is_vowel(next_syllable[0]):
                # Move last consonant to next syllable (Simple case)
                carry_over = syllable[-1]
                syllable = syllable[:-1]
            else:
                # Complex case
                consonant_cluster = ''.join(filter(is_consonant, syllable))
                if len(consonant_cluster) > 1:
                    carry_over = consonant_cluster[1:]
                    syllable = syllable.replace(consonant_cluster, consonant_cluster[0], 1)

        reshuffled_syllables.append(syllable)

    # Add any remaining carry over to the last syllable
    if carry_over:
        reshuffled_syllables[-1] += carry_over

    return reshuffled_syllables

def final_reshuffle(reshuffled_syllables):
    final_syllables = []
    
    for i, syllable in enumerate(reshuffled_syllables):
        # Check for the end of the syllable having multiple consonants
        if syllable and i < len(reshuffled_syllables) - 1 and is_consonant(syllable[-1]):
            next_syllable = reshuffled_syllables[i + 1]
            # Count how many consonants are at the end
            consonant_count = 0
            while consonant_count < len(syllable) and is_consonant(syllable[-(consonant_count + 1)]):
                consonant_count += 1
            
            if consonant_count > 1:
                # Leave one consonant at the end of the current syllable, push the rest to the next
                split_index = consonant_count - 1
                final_syllables.append(syllable[:-split_index])
                reshuffled_syllables[i + 1] = syllable[-split_index:] + next_syllable
            else:
                final_syllables.append(syllable)
        else:
            final_syllables.append(syllable)

    return final_syllables


def definitive_syllables(reshuffled_syllables):
    if not reshuffled_syllables:
        return reshuffled_syllables
    
    # If the first syllable is all consonants, join it with the second syllable
    if reshuffled_syllables[0] and not is_vowel(reshuffled_syllables[0][0]):
        if len(reshuffled_syllables) > 1:
            reshuffled_syllables[0] += reshuffled_syllables[1]
            reshuffled_syllables.pop(1)
    return reshuffled_syllables

def process_json_file(input_file_path, output_file_path):
    # Load the JSON file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Process each tragedy in the JSON file
    for tragedy in data:
        # Check and process each line in the tragedy
        if "lines" in tragedy:
            for line in tragedy["lines"]:
                # Check if 'divided_text' exists in the line
                if "divided_text" in line:
                    divided_text = line["divided_text"]
                    syllabified_text = syllabify(divided_text)
                    reshuffled_text = reshuffle_consonants(syllabified_text)
                    final_reshuffled_text = final_reshuffle(reshuffled_text)
                    definitive_text = definitive_syllables(final_reshuffled_text)

                    # Add 'syllabified_text' to the line
                    line["syllabified_text"] = ' '.join(definitive_text)

    # Write the modified data to a new JSON file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Path to the input JSON file
input_file_path = "/Users/ericu950/Documents/GitHub/DionysiusRecomposed/Source/2_Processed_JSON/tragedies_divided.json"
# Path to the output JSON file
output_file_path = "/Users/ericu950/Documents/GitHub/DionysiusRecomposed/Source/2_Processed_JSON/tragedies_syllabified.json"

# Process the JSON file and write to a new file
process_json_file(input_file_path, output_file_path)