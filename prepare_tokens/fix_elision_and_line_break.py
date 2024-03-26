'''
Fixes elided tokens whose elision signs have become separate tokens, 
as well as words with intra-word line breaks which have been triply tokenized: first part of the word + en dash + last part.

### CONTEXT AND THEORY ###

To understand the way in which the tokens have been extracted and the artifacts created thereby is crucial.
Take as an exampe Soph. Ajax 699f, Νύσια Κνώσι᾽ ὀρχήματ᾽ αὐτοδαῆ ξυνὼν ἰάψῃς:

Νύσια	a-p---na-	Νύσιος
Κνώσι	n-p---na-	Κνώσι
’	n-p---na-	’
ὀρ	n-p---na-	ὀρ
-	u--------	-
χήματ	n-p---na-	χήματ
’	n-p---na-	’
αὐτοδαῆ	a-p---na-	αὐτοδαής
ξυνὼν	v-sppamn-	ξυνὼν
ἰάψῃς	v2sasa---	ἰάπτω

Obviously, words followed by a line with an elision mark, need to be reunited with this mark (Κνώσι, χήματ + ’),
and words encircling a line-break mark need to be joined together (ὀρ + χήματ):

Νύσια	a-p---na-	Νύσιος
Κνώσι’	n-p---na-	Κνώσι
ὀρχήματ’	n-p---na-	ὀρχήματ’
αὐτοδαῆ	a-p---na-	αὐτοδαής
ξυνὼν	v-sppamn-	ξυνὼν
ἰάψῃς	v2sasa---	ἰάπτω

Now, the use of dashes for ellipses could have created confusion, as e.g. Eur. IT 1, 23, "τίκτει — τὸ καλλιστεῖον εἰς ἔμ᾽ ἀναφέρων —"

—	u--------	—
τὸ	l-s---na-	ὁ
καλλιστεῖον	n-s---na-	καλλιστεῖον
εἰς	r--------	εἰς
ἔμ	p-s---ma-	ἔμ
’	p-s---ma-	’
ἀναφέρων	v-sppamn-	ἀναφέρω
—	u--------	—

Luckily, the two usages have (hopefully consistently!) separate unicodes: the line-break is a short en dash, same as in the tag,
while the ellipsis is surrounded by two em dashes. 

WHAT IS ELISION IN GREEK?

In polysyllabic words, all final short vowels except ypsilon (CGCG 1.36) may be elided sometimes: α (ἆρ᾽), ε (ὅτε), ι (ἔστ᾽), ο (ἀφ᾽ οὗ).
In monosyllabic, only epsilon. For an example in action from the Aeschylean corpus, see: 

    ἔτ᾽ ἆρ᾽ Ἀθηνῶν ἔστ᾽ ἀπόρθητος πόλις; (Pers. 348)

Elided tokens which, like "ἵστημ", lack indicating apostrophe but fail to end on vowel or ν, ρ, σ, ξ, ψ,
need go through the same check as elisions with apostrophes. Elided words are found by these means: 
    - RIGHT SINGLE QUOTATION MARK (or alt. MODIFIER LETTER APOSTROPHE)
    - fail to end on all_vowels or r'[νξρςψ]' (= ends on r'[βγδζθκλμπστφχ]')
        NB: non-final sigma σ

ONLY AROUND 250 WORDS HAVE ELISION MARKS!
AROUND 2000 END ON βγδζθκλμπστφχ WITHOUT ELISION MARKS!
MORE ARE PROBABLY BE ELIDED BUT FORTUITIOUSLY END ON "CORRECT"


When it comes to prodelision with relevance for dichrona, we have e.g. 

στι	v3spia---	στι

Prodelisions do not seem to be marked in the corpus and/or not survive OdyCy, but I think there are very few relevant forms.


'''
import csv
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tqdm import tqdm

from utils import contains_greek, Colors

elision_chars = ('\u2019', '\u02BC') # RIGHT SINGLE QUOTATION MARK (’), the one used, but also MODIFIER LETTER APOSTROPHE (ʼ)


def broken_token(line1, line2, line3):
    """
    Takes as input three lines of tab-separated strings and returns True if:
    i) the tokens (first columns) of the first and the third lines contain Greek characters, and
    ii) the token of the second line consists only of an "en dash".
    """

    # Directly access the first token in each line
    token1 = line1[0] if len(line1) > 0 else ""
    token2 = line2[0] if len(line2) > 0 else ""
    token3 = line3[0] if len(line3) > 0 else ""

    # Check conditions
    condition1 = contains_greek(token1) and contains_greek(token3)
    condition2 = token2 == "-"  # This is a s.c. "hyphen-minus" (U+002D) and not the "en dash" (U+2013)

    return condition1 and condition2


def broken_elision(line1, line2):
    """
    Checks if the token in the first line contains Greek characters
    and if the token in the second line is one of the elision characters.

    Parameters:
    - line1: The first line of tab-separated strings.
    - line2: The second line of tab-separated strings.

    Returns:
    - True if conditions are met, False otherwise.
    """
    # Check if the first token contains Greek and the second token is an elision character
    if line1 and line2:  # Ensure lines are not empty
        token1_contains_greek = contains_greek(line1[0]) if len(line1) > 0 else False
        token2_is_elision_char = line2[0] in elision_chars if len(line2) > 0 else False

        return token1_contains_greek and token2_is_elision_char
    return False


def process_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as infile:
        lines = [line.strip() for line in infile]
    
    # Apply broken_elision and gather modified lines
    elision_count = 0
    i = 0
    while i < len(lines) - 1:
        line1 = lines[i].split('\t')
        line2 = lines[i+1].split('\t')
        if broken_elision(line1, line2):
            lines[i] = "\t".join([line1[0] + line2[0]] + line1[1:])
            lines.pop(i+1)  # Remove the next line as it's merged
            elision_count += 1
        else:
            i += 1

    # After fixing elisions, prepare for the next step
    modified_lines = lines.copy()  # Work on a copy of the modified lines after elision fixes

    # Apply broken_token on modified lines and fix token breaks
    token_count = 0
    i = 0
    while i < len(modified_lines) - 2:
        line1 = modified_lines[i].split('\t')
        line2 = modified_lines[i+1].split('\t')
        line3 = modified_lines[i+2].split('\t')
        if broken_token(line1, line2, line3):
            # Merge line1 and line3 and skip line2 and line3 in the next iteration
            modified_line = "\t".join([line1[0] + line3[0]] + line1[1:])
            modified_lines[i] = modified_line  # Replace line1 with the merged line
            del modified_lines[i+1:i+3]  # Remove line2 and line3 from the list
            token_count += 1
        else:
            i += 1  # Only increment if no token break was fixed

    # Write the final modified lines to the output file
    with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
        for line in tqdm(modified_lines, desc="Writing to output"):
            outfile.write(line + '\n')

    # Write modified lines to output file
    with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
        for line in modified_lines:
            outfile.write(line + '\n')

    print(f"{Colors.GREEN}Elisions fixed: {elision_count}. Token breaks fixed: {token_count}.{Colors.ENDC}")
    print(f"{Colors.GREEN}Process complete. Output written to {output_file_path}{Colors.ENDC}")


# Example usage
input_file_path = 'prepare_tokens/tokens/tragedies_300595.txt'  # Your input file path
output_file_path = 'prepare_tokens/tokens/tragedies_300595_fix_elision_hyphen.txt'  # Your output file path
process_file(input_file_path, output_file_path)