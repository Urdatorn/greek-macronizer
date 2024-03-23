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
    elision_chars = ('\u2019', '\u02BC') # RIGHT SINGLE QUOTATION MARK (’), the one used, but also MODIFIER LETTER APOSTROPHE (ʼ)
    incorrect_final_consonants = ('β', 'γ', 'δ', 'ζ', 'θ', 'κ', 'λ', 'μ', 'π', 'σ', 'τ', 'φ', 'χ')
    any_sign_of_elision = elision_chars + incorrect_final_consonants
    
    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
         open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in input_file:
            columns = line.split('\t')
            if columns[0].endswith(any_sign_of_elision):
                output_file.write(line)

# Example usage
input_file_path = 'prepare_tokens/tokens/tokens.txt'  # Update this to your actual input file path
output_file_path = 'tokens_elided.txt'  # The path where you want to save the filtered lines
elided_tokens(input_file_path, output_file_path)
