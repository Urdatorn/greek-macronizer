'''
Filters out elided tokens. 

These then need to be collated with their eventual unelided corresponding tokens.
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

from utils import all_vowels, Colors


def elided_tokens(input_file_path, output_file_path):
    elision_char1 = '\u2019' # RIGHT SINGLE QUOTATION MARK (’), the one used
    elision_char2 = '\u02BC' # MODIFIER LETTER APOSTROPHE (ʼ); there are no instances of this in the corpus; for clarity only
    incorrect_final_consonants = ('β', 'γ', 'δ', 'ζ', 'θ', 'κ', 'λ', 'μ', 'π', 'σ', 'τ', 'φ', 'χ')

    elision_char1_count = 0
    elision_char2_count = 0
    incorrect_consonant_count = 0

    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
         open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in input_file:
            columns = line.strip().split('\t')
            if columns and columns[0].endswith(elision_char1):
                elision_char1_count += 1
                output_file.write(line)
            elif columns and columns[0].endswith(elision_char2):
                elision_char2_count += 1
                output_file.write(line)
            elif columns and any(columns[0].endswith(consonant) for consonant in incorrect_final_consonants):
                incorrect_consonant_count += 1
                output_file.write(line)

    print(f"{Colors.GREEN}Lines ending with elision character 1 (’): {elision_char1_count}{Colors.ENDC}")
    print(f"{Colors.GREEN}Lines ending with elision character 2 (ʼ): {elision_char2_count}{Colors.ENDC}")
    print(f"{Colors.GREEN}Lines ending with incorrect final consonants: {incorrect_consonant_count}{Colors.ENDC}")


# Usage
input_file_path = 'prepare_tokens/tokens/tragedies_300595_fix_elision_hyphen_manualfix.txt'  # Update this to your actual input file path
output_file_path = 'tokens_elided.txt'  # The path where you want to save the filtered lines
elided_tokens(input_file_path, output_file_path)
