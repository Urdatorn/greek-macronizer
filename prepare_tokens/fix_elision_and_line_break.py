'''
Fixes:
    - elided tokens whose elision signs have become separate tokens, 
    - words with intra-word line breaks which have been triply tokenized: first part of the word + en dash + last part,
    - words with parts that are conjectures in angular brackets

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

The third needed fix is exemplified by S. OC 1733,
    "ἄγε με, καὶ τότ᾽ ἐπενάριξον":

    Ἄγε	v3siia---	ἄγω
    με	p-s---ma-	ἐγώ
    ,	u--------	,
    καὶ	c--------	καί
    τότ’	d--------	τότ
    <	d--------	<
    ἐπ	r--------	ἐπ
    >	d--------	>
    ενάριξον	v1saia---	ενάριξον
    .	u--------	.

 An editor has conjectured to add the prefix 'ἐπι' to 'ἐνάριξον' (ἐναρίζω, killing someone to take their ἔνᾰρα, "spoils"),
 and the conjectural part is written with <ἐπι>. This means the rest of the word lacks a spiritus, which is how this bug is found. 
 We need to remove the <> and join the two lines. The result should thus be

    Ἄγε	v3siia---	ἄγω
    με	p-s---ma-	ἐγώ
    ,	u--------	,
    καὶ	c--------	καί
    τότ’	d--------	τότ
    ἐπενάριξον	v1saia---	ἐπενάριξον
    .	u--------	.

Another example is:

    ξ	d--------	ἔξ
    <	u--------	<
    ίφει	v3spia---	ίφω
    >	u--------	>

which clearly should simply be

    ξίφει	v3spia---	ξίφει

An extra complicated case is S. Ant. 836

    Καίτοι	d--------	καίτοι
    φθιμένῃ	v-sapmfn-	φθιμένῃ
    μέγ	a-s---na-	μέγ
    <	d--------	<
    α	p-p---na-	α
    κ>ἀκοῦσαι	v--ana---	κ>ἀκοῦω

    Ἀλλὰ θεός τοι καὶ θεογεννής


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
import re
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tqdm import tqdm

from utils import contains_greek, with_spiritus, all_vowels, Colors

elision_chars = ('\u2019', '\u02BC') # RIGHT SINGLE QUOTATION MARK (’), the one used, but also MODIFIER LETTER APOSTROPHE (ʼ)


### AUXILIARY DEFINITIONS


def lacks_spiritus(word):
    """
    Checks if the first character of the word is a vowel and
    if the word does not contain any characters with spiritus.
    """
    if re.match(all_vowels, word[0]) and not re.search(with_spiritus, word):
        #print(word)
        return True
    return False


print(lacks_spiritus('ίφει'))
print(lacks_spiritus('ενάριξον'))


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


def broken_conjecture(line1, line2, line3, line4):
    """
    Given four lists as input, checks if the pattern for a broken conjecture is present.

    Parameters:
    - line1, line2, line3, line4: Lists representing tab-separated strings from consecutive lines.

    Returns:
    - True if the pattern matches for a broken conjecture; False otherwise.
    """
    condition1 = line1[0] == '<' and line3[0] == '>' and contains_greek(line2[0]) and lacks_spiritus(line4[0])
    condition2 = line2[0] == '<' and line4[0] == '>' #and contains_greek(line1[0]) and lacks_spiritus(line3[0])
    if len(line1) > 0 and len(line2) > 0 and len(line3) > 0 and len(line4) > 0:
        if condition1:
            print(line1)
            return 'Case 1'
        elif condition2:
            return 'Case 2'
    else:
        return False

### MAIN


def process_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as infile:
        lines = [line.strip() for line in infile]

    elision_count = 0
    token_count = 0
    conjecture_count = 0
    final_lines = []

    # First pass for broken_elision
    i = 0
    while i < len(lines) - 1:
        line1 = lines[i].split('\t')
        line2 = lines[i + 1].split('\t')
        if broken_elision(line1, line2):
            combined_line = "\t".join([line1[0] + line2[0]] + line1[1:])
            final_lines.append(combined_line)
            elision_count += 1
            i += 2  # Skip the next line as it's merged
        else:
            final_lines.append(lines[i])
            i += 1

    # Second pass for broken_token on the result of the first pass
    i = 0
    lines = final_lines  # Reset lines with results from first pass
    final_lines = []  # Reset final_lines for second pass
    while i < len(lines) - 2:
        line1 = lines[i].split('\t')
        line2 = lines[i + 1].split('\t')
        line3 = lines[i + 2].split('\t')
        if broken_token(line1, line2, line3):
            combined_line = "\t".join([line1[0] + line3[0]] + line1[1:])
            final_lines.append(combined_line)
            token_count += 1
            i += 3  # Skip the next two lines as they're merged
        else:
            final_lines.append(lines[i])
            i += 1

    # Third pass for broken_conjecture on the result of the second pass
    lines = final_lines  # Reset lines with results from second pass
    final_lines = []  # Reset final_lines for third pass
    i = 0
    while i < len(lines) - 3:
        line1 = lines[i].split('\t')
        line2 = lines[i + 1].split('\t')
        line3 = lines[i + 2].split('\t')
        line4 = lines[i + 3].split('\t')
        conjecture_result = broken_conjecture(line1, line2, line3, line4)
        if conjecture_result == 'Case 1':
            combined_line = "\t".join([line2[0] + line4[0], line2[1], line2[0] + line4[0]])
            final_lines.append(combined_line)
            conjecture_count += 1
            i += 4  # Skip the lines involved in the conjecture fix
        elif conjecture_result == 'Case 2':
            combined_line = "\t".join([line1[0] + line3[0], line1[1], line1[0] + line3[0]])
            final_lines.append(combined_line)
            conjecture_count += 1
            i += 4  # Skip the lines involved in the conjecture fix
        else:
            final_lines.append(lines[i])
            i += 1

    # Append any remaining lines that weren't part of a broken_conjecture group
    while i < len(lines):
        final_lines.append(lines[i])
        i += 1

    # Write the final lines to the output file
    with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
        for line in tqdm(final_lines, desc="Writing to output"):
            outfile.write(line + '\n')

    print(f"{Colors.GREEN}Elisions fixed: {elision_count}. Token breaks fixed: {token_count}. Conjectures fixed: {conjecture_count}.{Colors.ENDC}")
    print(f"{Colors.GREEN}Process complete. Output written to {output_file_path}{Colors.ENDC}")


# Example usage
#input_file_path = 'prepare_tokens/tokens/tragedies_300595.txt'  # Your input file path
#output_file_path = 'prepare_tokens/tokens/tragedies_300595_fix_elision_hyphen.txt'  # Your output file path
    
input_file_path = 'prepare_tokens/tokens/test_elision2.txt'
output_file_path = 'prepare_tokens/tokens/test_elision_output2.txt'
process_file(input_file_path, output_file_path)