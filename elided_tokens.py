'''
Filters out elided tokens. 

These then need to be collated with their eventual unelided corresponding tokens.
In polysyllabic words, all final short vowels except ypsilon (CGCG 1.36) may be elided sometimes: α (ἆρ᾽), ε (ὅτε), ι (ἔστ᾽), ο (ἀφ᾽ οὗ).
In monosyllabic, only epsilon. For an example in action from the Aeschylean corpus, see: 

ἔτ᾽ ἆρ᾽ Ἀθηνῶν ἔστ᾽ ἀπόρθητος πόλις; (Pers. 348)

Elided tokens which, like "ἵστημ", lack indicating apostrophe but fail to end on vowel or ν, ρ, σ, ξ, ψ,
need go through the same check as elisions with apostrophes.

When it comes to prodelision with relevance for dichrona, we have e.g. 

στι	v3spia---	στι

Prodelisions do not seem to be marked in the corpus and/or not survive OdyCy, but I think there are very few relevant forms.


'''

def elided_tokens(input_file_path, output_file_path):
    # Define the characters to check for at the end of the first column
    target_chars = ('\u2019', '\u02BC') # RIGHT SINGLE QUOTATION MARK (’), the one used, but also MODIFIER LETTER APOSTROPHE (ʼ)
    
    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
         open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in input_file:
            # Split the line into columns based on tabs
            columns = line.split('\t')
            # Check if the first column ends with any of the target characters
            if columns[0].endswith(target_chars):
                # Write the line to the output file
                output_file.write(line)

# Example usage
input_file_path = 'prepare_tokens/tokens/tokens.txt'  # Update this to your actual input file path
output_file_path = 'tokens_elided.txt'  # The path where you want to save the filtered lines
elided_tokens(input_file_path, output_file_path)
