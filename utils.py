'''
/utils.py

Classes, sets and constants for use in many scripts
'''

import re
from pyuca import Collator
from greek_accentuation.characters import base

from erics_syllabifier import syllabifier

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


###### REGULAR EXPRESSIONS ######


# GREEK ALPHABET CHARACTERS

base_alphabet = r'[ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρσςτυφχψω]' # 24 uppercase, 25 lowercase

def only_bases(word):
    '''
    E.g. ᾰ̓ᾱ́ᾰτᾰ returns ααατα.
    Dependencies: greek_accentuation.characters.base and re
    '''
    return ''.join([base(char) for char in word if re.search(base_alphabet, base(char))])


def initial_base(word):
    '''
    Takes a word and returns the base of the first character joined with the rest of the word from the second character onward.
    E.g. ᾰ̓ᾱ́ᾰτᾰ returns αᾱ́ᾰτᾰ.
    '''
    if not word:  # Check if the word is empty
        return word
    return base(word[0]) + word[1:]


def sort_polytonic_string(input_string):
    c = Collator()

    characters = list(input_string)
    sorted_characters = sorted(characters, key=lambda char: c.sort_key(char))
    sorted_string = ''.join(sorted_characters)

    return sorted_string


# VOWELS
# note that rn these don't include all capital letters
# the vast number of dichrona with VRACHY/LONGA + other diacritics are in crawl_wiktionary/macrons_map.py

iotas = r'[ιϊἰἱίΐἴἵὶῒἲἳῖῗἶἷΙἸἼἺἾἹἽἻἿΊῚΪῐῘῑῙ]'

iota_in_diphthong = r'[ιἰἱίἴἵὶἲἳῖἶἷ]' # NB: if any of these iotas follows an accent- and spiritusless α,ε,ο,υ or any η,ω, it is the second part of a diphthong and should not be macronized
iota_diaeresis = r'[ϊΐῒῗΪ]'

acutes = r'[άέήίόύώΐΰἄἅἔἕἤἥἴἵὄὅὔὕὤὥᾄᾅᾴᾔᾕῄᾤᾥῴ]' # problem with how to represent capital iota adscript; cf. Eric's regex
graves = r'[ὰὲὴὶὸὺὼῒῢἂἃἒἓἢἣἲἳὂὃὒὓὢὣᾂᾃᾲᾒᾓῂᾢᾣῲ]'
circumflexes = r'[ᾶῆῖῦῶῗῧἇἆἦἧἶἷὖὗὦὧἦἧἆἇὧὦᾆᾇᾷᾖᾗᾦᾧῷῇ]'
all_accents = f'[{acutes[1:-1]}{graves[1:-1]}{circumflexes[1:-1]}]' # sum of above 3

unaccented = r'[αεηιουωϊϋἀἁἐἑἠἡἰἱὀὁὐὑὠὡᾳᾀᾁῃᾐᾑῳᾠᾡ]' # 7 + 14 + 9
all_vowels_lowercase = f'[{all_accents[1:-1]}{unaccented[1:-1]}]' # sum of above 2; NB: no iota adscript
all_vowels_uppercase = r'[ΑἈἌἊἎἉἍἋἏΆᾺΕἘἜἚἙἝἛΈῈΗἨἬἪἮἩἭἫἯΉῊΙἸἼἺἾἹἽἻἿΊῚΪΟὈὌὊὉὍὋΌῸΥὙὝὛὟΎῪΫΩὨὬὪὮὩὭὫὯΏῺᾬᾪᾮᾨᾭᾫᾯᾩῼ]' 
'''
NB: the wiktionary crawl includes nine characters of omega with what appears as iota subscript, which is rather unusual. 71 characters. This string was generated by the .upper() method and functions removing duplicates and pyuca sorting.
'''
all_vowels = f'[{all_vowels_lowercase[1:-1]}{all_vowels_uppercase[1:-1]}]' # sum of above 2

with_spiritus = r'[ἈἉἘἙἨἩἸἹὈὉὙὨὩἀἁἐἑἠἡἰἱὀὁὐὑὠὡᾀᾁᾐᾑᾠᾡἄἅἔἕἤἥἴἵὄὅὔὕὤὥᾄᾅᾔᾕᾤᾥἂἃἒἓἢἣἲἳὂὃὒὓὢὣᾂᾃᾒᾓᾢᾣἇἆἦἧἶἷὖὗὦὧἦἧἆἇὧὦᾆᾇᾖᾗᾦᾧ]'
without_spiritus = r'[αάὰᾶεέὲηήὴῆιίὶῖϊΐῒῗοόὸυύὺῦϋΰῢῧωώὼῶ]' # pyuca sorted + no duplicates

longa_brevi = r'[ᾰᾸᾱᾹῐῘῑῙῠῨῡῩ]'

def upper(λέξις):
    upper = λέξις.upper()
    return upper

def lower(λέξις):
    lower = λέξις.lower()
    return lower


# CONSONANTS
# there are 18 capital consonants, if we include both aspirated and spiritus-less ῥῶ (it's always aspirated at word beginning, so only all-caps would have it spiritus-less, which is rare but exists in prosopa dramatis). There is no spiritus lenis capital rho in unicode.
# there are 2 lowercase sigmas and all 3 rhos, so 20
# ergo totally 18 + 20 = 38
# NB: digamma ϝ is not used in the tragic corpus used here, but exists in wiktionary etc.
all_consonants = r'[ΒΓΔΖΘΚΛΜΝΞΠΡῬΣΤΦΧΨβγδζθκλμνξπρῤῥσςτφχψ]' 
# indigenous Greek words in Attic ended on vowel or one of 5 consonants, e.g. ἐάν, σάρξ, κήρ, ὗς, φλέψ. Of course, phonetically three of these really end on /s/ and none of them are stops.
# there are a few exceptional forms on κ as well, such as ἐκ, οὐκ, which depend on context and are better treated as stop words than as part of the regex.
# in dialects and Homer there are *tons* of exceptions due to apocope, assimilation etc.
legitimate_final_consonants = r'[νξρςψ]' # excluding οὐκ, ἐκ, κἀκ (crasis for καὶ ἐκ) etc.
illegitimate_final_consonants = r'[βγδζθκλμπστφχ]'


### some functions using the regexes ###


def open_syllable(syllable):
    base_form = only_bases(syllable)
    if base_form and base_form[-1] in all_vowels_lowercase:
        return syllable
    return None


###### STRING LITERALS ######


# Unicode Constants for Ancient Greek punctuation
class Punctuation:
    GREEK_ANO_TELEIA = '\u0387'
    MIDDLE_DOT = '\u00b7' # preferred by Taubner
    GREEK_QUESTION_MARK = '\u037E' 
    SEMICOLON = '\u003b' # preferred by Taubner
    DAGGER = '\u2020'
    EM_DASH = '\u2014'
    EN_DASH = '\u2013'
    MULTIPLICATION_SIGN = '\u00d7'
    COMMA = ','
    PERIOD = '.'
    ANGULAR_BRACKET_LEFT = '<'
    ANGULAR_BRACKET_RIGHT = '>'
    SQUARE_BRACKET_LEFT = '['
    SQUARE_BRACKET_RIGHT = ']'


class Elision:
    ELISION1 = '\u2019' # "right single quotation mark". Preferred by Taubner
    ELISION2 = '\u02BC' # "modifier letter apostrophe"

# Dynamically create a set of all punctuation characters defined in the Punctuation class
punctuation_chars_set = set(getattr(Punctuation, attr) for attr in dir(Punctuation) if not attr.startswith("__"))

# Unicode ranges for Greek characters
MONOTONIC_CHARS = set(range(0x391, 0x3A9 + 1)).union(range(0x3B1, 0x3C9 + 1))
POLYPHONIC_CHARS = set(range(0x1F00, 0x1FFF + 1))

# Merge both sets for a unified set of Greek characters, and remove the punctuation
GREEK_CHARS = (MONOTONIC_CHARS.union(POLYPHONIC_CHARS)) - punctuation_chars_set

ACCENTS = {
    '\u0384',  # ΄: GREEK TONOS
    '\u0385',  # ΅: GREEK DIALYTIKA TONOS
    '\u0387',  # ·: GREEK ANO TELEIA
    '\u1fbd',  # ᾽: GREEK KORONIS
    '\u1fbe',  # ι: GREEK PROSGEGRAMMENI
    '\u1fbf',  # ᾿: GREEK PSILI
    '\u1fc0',  # ῀: GREEK PERISPOMENI
    '\u1fc1',  # ῁: GREEK DIALYTIKA AND PERISPOMENI
    '\u1fcd',  # ῍: GREEK PSILI AND VARIA
    '\u1fce',  # ῎: GREEK PSILI AND OXIA
    '\u1fcf',  # ῏: GREEK PSILI AND PERISPOMENI
    '\u1fdd',  # ῝: GREEK DASIA AND VARIA
    '\u1fde',  # ῞: GREEK DASIA AND OXIA
    '\u1fdf',  # ῟: GREEK DASIA AND PERISPOMENI
    '\u1fed',  # ῭: GREEK DIALYTIKA AND VARIA
    '\u1fee',  # ΅: GREEK DIALYTIKA AND OXIA
    '\u1fef',  # `: GREEK VARIA
    '\u1ffd',  # ´: GREEK OXIA
    '\u1ffe',  # ῾: GREEK DASIA
    '\u0301',  #  ́: COMBINING ACUTE ACCENT
    '\u0308',  #  ̈: COMBINING DIAERESIS
    '\u035C',  #  ͜: COMBINING DOUBLE BREVE BELOW
    '\u0300',  #  ̀: COMBINING GRAVE ACCENT
    '\u0313',  #  ̓: COMBINING COMMA ABOVE
    '\u032F',  #  ̯: COMBINING INVERTED BREVE BELOW
    '\u0314',  #  ̔: COMBINING REVERSED COMMA ABOVE
    '\u0312',  #  ̒: COMBINING TURNED COMMA ABOVE
    '\u0345',  #  ͅ: COMBINING GREEK YPOGEGRAMMENI
    '\u0342',  #  ͂: COMBINING GREEK PERISPOMENI
}


def contains_greek(text):
    """
    Check if the provided text contains any Greek characters.
    
    Args:
        text (str): The text string to be checked for Greek characters.
    
    Returns:
        bool: True if the text contains any Greek characters, False otherwise.
    """
    return any(char in GREEK_CHARS for char in map(ord, text))

'''
All true DICHRONA, i.e. letters that may hide quantity.
The following AIY in cltk are excluded as unnecessary: 
- capitals without spiritus (can't appear in AG)
- iota subscriptum forms (always long)
- the six macronized lower-case forms without other diacritics (our corpus analysandum is not macronized)
- circumflexes (always long)

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

NB3 that the following ypsilons are not in the unicode Greek Extended: ᾽Υ, ῍Υ, ῎Υ ῏Υ. See https://www.opoudjis.net/unicode/unicode_gaps.html#gaps

NB3 that polytonic Greek (Greek Extended) escape codes start with 'u1f' (they lie in 1F00—1FFF) whereas monotonic starts with 'u3'.
Use hex(ord('x')) to get a character x's escape code and chr(0x123) to show the character coded by hex string '0x123'.
'''
DICHRONA = {
    # CAPITALS
    "\u1f08",  # Ἀ Greek Capital Letter Alpha with Psili
    "\u1f38",  # Ἰ Greek Capital Letter Iota with Psili

    "\u1f0c",  # Ἄ Greek Capital Letter Alpha with Psili and Oxia
    "\u1f3c",  # Ἴ Greek Capital Letter Iota with Psili and Oxia

    "\u1f0a",  # Ἂ Greek Capital Letter Alpha with Psili and Varia
    "\u1f3a",  # Ἲ Greek Capital Letter Iota with Psili and Varia

    "\u1f09",  # Ἁ Greek Capital Letter Alpha With Dasia
    "\u1f39",  # Ἱ Greek Capital Letter Iota With Dasia
    "\u1f59",  # Ὑ Greek Capital Letter Upsilon With Dasia

    "\u1f0d",  # Ἅ Greek Capital Letter Alpha With Dasia And Oxia
    "\u1f3d",  # Ἵ Greek Capital Letter Iota With Dasia And Oxia
    "\u1f5d",  # Ὕ Greek Capital Letter Upsilon With Dasia And Oxia

    "\u1f0b",  # Ἃ Greek Capital Letter Alpha With Dasia And Varia
    "\u1f3b",  # Ἳ Greek Capital Letter Iota With Dasia And Varia
    "\u1f5b",  # Ὓ Greek Capital Letter Upsilon With Dasia And Varia

    # LOWER-CASE (NB 3 overlapping tonos-oxia)
    "\u03b1",  # α Greek Small Letter Alpha
    "\u03b9",  # ι Greek Small Letter Iota
    "\u03c5",  # υ Greek Small Letter Upsilon

    "\u03ac",  # ά Greek Small Letter Alpha With Tonos
    "\u03af",  # ί Greek Small Letter Iota With Tonos
    "\u03cd",  # ύ Greek Small Letter Upsilon With Tonos

    "\u1f71",  # ά Greek Small Letter Alpha With Oxia
    "\u1f77",  # ί Greek Small Letter Iota With Oxia
    "\u1f7b",  # ύ Greek Small Letter Upsilon With Oxia

    "\u1f70",  # ὰ Greek Small Letter Alpha With Varia
    "\u1f76",  # ὶ Greek Small Letter Iota With Varia
    "\u1f7a",  # ὺ Greek Small Letter Upsilon With Varia

    "\u1f00",  # ἀ Greek Small Letter Alpha With Psili
    "\u1f30",  # ἰ Greek Small Letter Iota With Psili
    "\u1f50",  # ὐ Greek Small Letter Upsilon With Psili

    "\u1f04",  # ἄ Greek Small Letter Alpha With Psili And Oxia
    "\u1f34",  # ἴ Greek Small Letter Iota With Psili And Oxia
    "\u1f54",  # ὔ Greek Small Letter Upsilon With Psili And Oxia

    "\u1f02",  # ἂ Greek Small Letter Alpha With Psili And Varia
    "\u1f32",  # ἲ Greek Small Letter Iota With Psili And Varia
    "\u1f52",  # ὒ Greek Small Letter Upsilon With Psili And Varia

    "\u1f01",  # ἁ Greek Small Letter Alpha With Dasia
    "\u1f31",  # ἱ Greek Small Letter Iota With Dasia
    "\u1f51",  # ὑ Greek Small Letter Upsilon With Dasia

    "\u1f05",  # ἅ Greek Small Letter Alpha With Dasia And Oxia
    "\u1f35",  # ἵ Greek Small Letter Iota With Dasia And Oxia
    "\u1f55",  # ὕ Greek Small Letter Upsilon With Dasia And Oxia

    "\u1f03",  # ἃ Greek Small Letter Alpha With Dasia And Varia
    "\u1f33",  # ἳ Greek Small Letter Iota With Dasia And Varia
    "\u1f53",  # ὓ Greek Small Letter Upsilon With Dasia And Varia

    # DIAERESIS/TREMA/DIALYTIKA (NB 2 overlapping tonos-oxia)
    "\u03ca",  # ϊ Greek Small Letter Iota With Dialytika
    "\u03cb",  # ϋ Greek Small Letter Upsilon With Dialytika

    "\u0390",  # ΐ Greek Small Letter Iota With Dialytika And Tonos
    "\u03b0",  # ΰ Greek Small Letter Upsilon With Dialytika And Tonos

    "\u1fd3",  # ΐ Greek Small Letter Iota With Dialytika And Oxia; my addition
    "\u1fe3",  # ΰ Greek Small Letter Iota With Dialytika And Oxia; my addition

    "\u1fd2",  # ῒ Greek Small Letter Iota With Dialytika And Varia
    "\u1fe2",  # ῢ Greek Small Letter Upsilon With Dialytika And Varia
}