base_macrons = {'ᾰ', 'Ᾰ', 'ᾱ', 'Ᾱ', 'ῐ', 'Ῐ', 'ῑ', 'Ῑ', 'ῠ', 'Ῠ', 'ῡ', 'Ῡ'}

combining_codes = {
    'U+0301': '',  # ́: COMBINING ACUTE ACCENT (U+0301)
    'U+0308': '',  # ̈: COMBINING DIAERESIS (U+0308)
    'U+035C': '',  # ͜: COMBINING DOUBLE BREVE BELOW (U+035C)
    'U+0300': '',  # ̀: COMBINING GRAVE ACCENT (U+0300)
    'U+0313': '',  # ̓: COMBINING COMMA ABOVE (U+0313)
    'U+032F': '',  # ̯: COMBINING INVERTED BREVE BELOW (U+032F)
    'U+0314': '',  # ̔: COMBINING REVERSED COMMA ABOVE (U+0314)
    'U+0312': '',  # ̒: COMBINING TURNED COMMA ABOVE (U+0312)
    'U+0345': '',  # ͅ: COMBINING GREEK YPOGEGRAMMENI (U+0345)
    'U+0342': '',  # ͂: COMBINING GREEK PERISPOMENI (U+0342)
}


def find_base_macron_combinations(input_file_path):
    # Define base macrons and combining marks
    base_macrons = {'ᾰ', 'Ᾰ', 'ᾱ', 'Ᾱ', 'ῐ', 'Ῐ', 'ῑ', 'Ῑ', 'ῠ', 'Ῠ', 'ῡ', 'Ῡ'}
    combining_codes = {
        '\u0301',  # COMBINING ACUTE ACCENT
        '\u0308',  # COMBINING DIAERESIS
        '\u035C',  # COMBINING DOUBLE BREVE BELOW
        '\u0300',  # COMBINING GRAVE ACCENT
        '\u0313',  # COMBINING COMMA ABOVE
        '\u032F',  # COMBINING INVERTED BREVE BELOW
        '\u0314',  # COMBINING REVERSED COMMA ABOVE
        '\u0312',  # COMBINING TURNED COMMA ABOVE
        '\u0345',  # COMBINING GREEK YPOGEGRAMMENI
        '\u0342',  # COMBINING GREEK PERISPOMENI
    }

    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    results = []
    
    # Iterate over characters in the text
    for i in range(len(text) - 1):
        current_char = text[i]
        next_char = text[i + 1]
        
        # Check if current character is a base macron and the next is a combining mark
        if current_char in base_macrons and next_char in combining_codes:
            combined_character = current_char + next_char
            results.append(combined_character)
            #print(f"Found combination: {combined_character} at position {i}")

    # Remove duplicates and sort by the composite characters using a collator
    from pyuca import Collator
    collator = Collator()
    sorted_results = sorted(set(results), key=lambda item: collator.sort_key(item))
    
    print("All unique combinations sorted:")
    for res in sorted_results:
        print(res)

# Example usage
input_file_path = 'crawl_wiktionary/macrons_wiktionary_raw.txt'
find_base_macron_combinations(input_file_path)
