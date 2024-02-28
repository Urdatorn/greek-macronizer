'''
/prepare_tokens/utils.py

Functions and constants for use during preparation of tokens.txt
'''

import re
import string
import unicodedata

class Colors:
    GREEN = '\033[1;32m'  # Green
    RED = '\033[1;31m'    # Red
    ENDC = '\033[0m'      # Reset to default color
    YELLOW = '\033[1;33m' # Yellow
    BLUE = '\033[1;34m'   # Blue
    MAGENTA = '\033[1;35m'# Magenta
    CYAN = '\033[1;36m'   # Cyan
    WHITE = '\033[1;37m'  # White
    BOLD = '\033[1m'      # Bold
    UNDERLINE = '\033[4m' # Underline

'''
All true DICHRONA, i.e. letters that may hide quantity.
The following AIY in cltk are excluded as unnecessary: 
- capitals without spiritus (can't appear in AG)
- iota subscriptum forms (always long)
- the six macronized lower-case forms without other diacritics (our corpus analysandum is not macronized)
- circumflexes

Commented names are official unicode, and tends to use Modern Greek linguistic vocabulary
NB that unicode calls
acute = 'oxia' for polytonic and 'tonos' for monotonic (only the small ones overlap with polytonic): we include both here, but for string comparisons we need to convert everything to oxia
grave = 'varia'
circumflex = 'perispomeni' (although these are not included)
spīritūs asperī and lēnēs = 'psili' and 'dasia'
iota adscriptum = 'prosgegrammeni' (the font in VSCode shows these as subscripta. Not sure whether these are widely used as opposed to just writing iotas)
iota subscriptum = 'ypogegrammeni' (although these are not included)
Greek diaeresis/trema = 'dialytika' (although on its own the diacritic is called 'combining diaeresis')
longum = 'macron'
breve = 'vrachy' (although these two are not included either).

NB2 that there are FIVE overlapping tonos-oxia glyphs: ά, ί, ύ, ΐ, ΰ.
The last two appear as  in the corpus (e.g. βαΰζει, Δαναΐδων) but are not included in cltk's tonos_oxia_converter,
so I will have to write my own. 

NB2 that the following ypsilons are not in the unicode Greek Extended: ᾽Υ, ῍Υ, ῎Υ ῏Υ. Why?

NB3 that polytonic Greek (Greek Extended) escape codes start with 'u1f' (they lie in 1F00—1FFF) whereas monotonic starts with 'u3'.
Use hex(ord('x')) to get a character x's escape code and chr(0x123) to show the character coded by hex string '0x123'.
'''
DICHRONA = set([
    # CAPITALS
    "\u1f08",  # Ἀ Greek Capital Letter Alpha with Psili
    "\u1f38",  # Ἰ Greek Capital Letter Iota with Psili
    "\u1f88",  # ᾈ Greek Capital Letter Alpha with Psili and Prosgegrammeni

    "\u1f0c",  # Ἄ Greek Capital Letter Alpha with Psili and Oxia
    "\u1f3c",  # Ἴ Greek Capital Letter Iota with Psili and Oxia
    "\u1f8c",  # ᾌ Greek Capital Letter Alpha with Psili and Oxia and Prosgegrammeni

    "\u1f0a",  # Ἂ Greek Capital Letter Alpha with Psili and Varia
    "\u1f3a",  # Ἲ Greek Capital Letter Iota with Psili and Varia
    "\u1f8a",  # ᾊ Greek Capital Letter Alpha With Psili And Varia And Prosgegrammeni

    "\u1f0e",  # Ἆ Greek Capital Letter Alpha With Psili And Perispomeni
    "\u1f3e",  # Ἶ Greek Capital Letter Iota With Psili And Perispomeni
    "\u1f8e",  # ᾎ Greek Capital Letter Alpha With Psili And Perispomeni And Prosgegrammeni

    "\u1f09",  # Ἁ Greek Capital Letter Alpha With Dasia
    "\u1f39",  # Ἱ Greek Capital Letter Iota With Dasia
    "\u1f59",  # Ὑ Greek Capital Letter Upsilon With Dasia
    "\u1f89",  # ᾉ Greek Capital Letter Alpha With Dasia And Prosgegrammeni

    "\u1f0d",  # Ἅ Greek Capital Letter Alpha With Dasia And Oxia
    "\u1f3d",  # Ἵ Greek Capital Letter Iota With Dasia And Oxia
    "\u1f5d",  # Ὕ Greek Capital Letter Upsilon With Dasia And Oxia
    "\u1f8d",  # ᾍ Greek Capital Letter Alpha With Dasia And Oxia And Prosgegrammeni

    "\u1f0b",  # Ἃ Greek Capital Letter Alpha With Dasia And Varia
    "\u1f3b",  # Ἳ Greek Capital Letter Iota With Dasia And Varia
    "\u1f5b",  # Ὓ Greek Capital Letter Upsilon With Dasia And Varia
    "\u1f8b",  # ᾋ Greek Capital Letter Alpha With Dasia And Varia And Prosgegrammeni
    
    "\u1f0f",  # Ἇ Greek Capital Letter Alpha With Dasia And Perispomeni
    "\u1f3f",  # Ἷ Greek Capital Letter Iota With Dasia And Perispomeni
    "\u1f5f",  # Ὗ Greek Capital Letter Upsilon With Dasia And Perispomeni
    "\u1f8f",  # ᾏ Greek Capital Letter Alpha With Dasia And Perispomeni And Prosgegrammeni

    "\u03aa",  # Ϊ Greek Capital Letter Iota With Dialytika
    "\u03ab",  # Ϋ Greek Capital Letter Upsilon With Dialytika

    # LOWER-CASE (NB 3 overlapping tonos-oxia)
    "\u03b1",  # α Greek Small Letter Alpha
    "\u03b9",  # ι Greek Small Letter Iota
    "\u03c5",  # υ Greek Small Letter Upsilon

    "\u03ac",  # ά Greek Small Letter Alpha With Tonos
    "\u03af",  # ί Greek Small Letter Iota With Tonos
    "\u03cd",  # ύ Greek Small Letter Upsilon With Tonos

    "\u1f71",  # ά Greek Small Letter Alpha With Oxia
    "\u1f77",  # ί Greek Small Letter Iota With Oxia
    "\u1f7b",  # ύ Greek Small Letter Upsilon With Oxiax

    "\u1f70",  # ὰ Greek Small Letter Alpha With Varia
    "\u1f76",  # ὶ Greek Small Letter Iota With Varia
    "\u1f7a",  # ὺ Greek Small Letter Upsilon With Varia

    "\u1fb6",  # ᾶ Greek Small Letter Alpha With Perispomeni
    "\u1fd6",  # ῖ Greek Small Letter Iota With Perispomeni
    "\u1fe6",  # ῦ Greek Small Letter Upsilon With Perispomeni

    "\u1f00",  # ἀ Greek Small Letter Alpha With Psili
    "\u1f30",  # ἰ Greek Small Letter Iota With Psili
    "\u1f50",  # ὐ Greek Small Letter Upsilon With Psili

    "\u1f04",  # ἄ Greek Small Letter Alpha With Psili And Oxia
    "\u1f34",  # ἴ Greek Small Letter Iota With Psili And Oxia
    "\u1f54",  # ὔ Greek Small Letter Upsilon With Psili And Oxia

    "\u1f02",  # ἂ Greek Small Letter Alpha With Psili And Varia
    "\u1f32",  # ἲ Greek Small Letter Iota With Psili And Varia
    "\u1f52",  # ὒ Greek Small Letter Upsilon With Psili And Varia

    "\u1f06",  # ἆ Greek Small Letter Alpha With Psili And Perispomeni
    "\u1f36",  # ἶ Greek Small Letter Iota With Psili And Perispomeni
    "\u1f56",  # ὖ Greek Small Letter Upsilon With Psili And Perispomeni

    "\u1f01",  # ἁ Greek Small Letter Alpha With Dasia
    "\u1f31",  # ἱ Greek Small Letter Iota With Dasia
    "\u1f51",  # ὑ Greek Small Letter Upsilon With Dasia

    "\u1f05",  # ἅ Greek Small Letter Alpha With Dasia And Oxia
    "\u1f35",  # ἵ Greek Small Letter Iota With Dasia And Oxia
    "\u1f55",  # ὕ Greek Small Letter Upsilon With Dasia And Oxia

    "\u1f03",  # ἃ Greek Small Letter Alpha With Dasia And Varia
    "\u1f33",  # ἳ Greek Small Letter Iota With Dasia And Varia
    "\u1f53",  # ὓ Greek Small Letter Upsilon With Dasia And Varia

    "\u1f07",  # ἇ Greek Small Letter Alpha With Dasia And Perispomeni
    "\u1f37",  # ἷ Greek Small Letter Iota With Dasia And Perispomeni
    "\u1f57",  # ὗ Greek Small Letter Upsilon With Dasia And Perispomeni

    # DIAERESIS/TREMA/DIALYTIKA (NB 2 overlapping tonos-oxia)
    "\u03ca",  # ϊ Greek Small Letter Iota With Dialytika
    "\u03cb",  # ϋ Greek Small Letter Upsilon With Dialytika

    "\u0390",  # ΐ Greek Small Letter Iota With Dialytika And Tonos
    "\u03b0",  # ΰ Greek Small Letter Upsilon With Dialytika And Tonos

    "\u1fd3",  # ΐ Greek Small Letter Iota With Dialytika And Oxia; my addition
    "\u1fe3",  # ΰ Greek Small Letter Iota With Dialytika And Oxia; my addition

    "\u1fd2",  # ῒ Greek Small Letter Iota With Dialytika And Varia
    "\u1fe2",  # ῢ Greek Small Letter Upsilon With Dialytika And Varia
 
    "\u1fd7",  # ῗ Greek Small Letter Iota With Dialytika And Perispomeni
    "\u1fe7",  # ῧ Greek Small Letter Upsilon With Dialytika And Perispomeni
])

def is_dichrona(char):
    return char in DICHRONA

def count_dichrona(word):
    return sum(is_dichrona(char) for char in word)

# Unicode Constants for Ancient Greek punctuation
GREEK_ANO_TELEIA = '\u0387'
MIDDLE_DOT = '\u00b7' # preferred by Taubner
GREEK_QUESTION_MARK = '\u037E' 
SEMICOLON = '\u003b' # preferred by Taubner
DAGGER = '\u2020'
EM_DASH = '\u2014'
# for elision etc.
ELISION1 = '\u2019' # "right single quotation mark". Preferred by Taubner
ELISION2 = '\u02BC' # "modifier letter apostrophe"

# Unicode ranges for Greek characters
MONOTONIC_CHARS = set(range(0x391, 0x3A9 + 1)).union(range(0x3B1, 0x3C9 + 1)) - {GREEK_ANO_TELEIA, MIDDLE_DOT, GREEK_QUESTION_MARK, SEMICOLON}
POLYPHONIC_CHARS = set(range(0x1F00, 0x1FFF + 1))

# Merge both sets for a unified set of Greek characters
GREEK_CHARS = MONOTONIC_CHARS.union(POLYPHONIC_CHARS)

# Function to remove surrounding punctuation and dagger from Greek characters
def remove_surrounding_punctuation(token_or_lemma):
    """
    Remove surrounding punctuation, including Greek-specific punctuation and dagger, from a token or lemma containing Greek characters.
    
    Args:
        token_or_lemma (str): The token or lemma from which surrounding punctuation and dagger are to be removed.
    
    Returns:
        str: The input string with surrounding punctuation and dagger removed, if present.
    """
    punctuation = string.punctuation + GREEK_ANO_TELEIA + MIDDLE_DOT + GREEK_QUESTION_MARK + SEMICOLON + DAGGER + EM_DASH
    pattern = r'^([' + re.escape(punctuation) + r']+)?(.*[\u0370-\u03ff\u1f00-\u1fff]+)([' + re.escape(punctuation) + r']+)?$'
    match = re.match(pattern, token_or_lemma)
    if match:
        return match.group(2)  # Return the part with Greek characters, excluding surrounding punctuation/dagger/em dash
    return token_or_lemma
