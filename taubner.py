'''
Functions I have use of from Taubner's package:

syllabify
(syllabify.is_vowel)
syllabify.is_diphthong
syllabify.ultima, penult, antepenult
syllabify.onset_nucleus_coda
accentuation.get_accent_type

OXYTONE implies nothing without context (cf. αἰδώς)
PAROXYTONE with ≥3 syllables still does NOT imply long vowel in ultima, because not all accents are recessive (cf. pf. ppc. λελῠμένος)
PROPAROXYTONE implies that the vowel in the ultima is short
PERISPOMENON implies that the vowel in the ultima is long (as all vowels with circumf.)
PROPERISPOMENON implies that the vowel in the ultima is short

USE OF syllabify.is_diphthong
- Filter out words that do not have any DICHRONA or only have DICHRONA in diphthongs

USE OF syllabify 
- Check for DICHRONA in open syllables, to be checked against the metrical corpora

'''

# syllabify module

from greek_accentuation.syllabify import syllabify

print(syllabify('γυναικός')) # ['γυ', 'ναι', 'κός']

from greek_accentuation.syllabify import is_vowel, is_diphthong, ultima, penult, antepenult, onset_nucleus_coda

print(is_vowel('κ')) # False
print(is_vowel('ακ')) # True; it's enough if the initial character of the string is a vowel

print(is_diphthong('αι')) # True
# Sucks horseshit, because e.g. is_diphthong('ἄι') comes out true!??!

print(ultima('πατρός')) # τρός, it sees muta cum liquida as single
print(antepenult('ποτιδέρκομαι')) # δέρ
print(penult('ποτιδέρκομαι')) # κο
print(ultima('ποτιδέρκομαι')) # μαι

print(onset_nucleus_coda('ναι')) # ('ν', 'αι', '')

# accentuation module

from greek_accentuation.accentuation import get_accent_type, OXYTONE, PAROXYTONE, PROPAROXYTONE, PERISPOMENON, PROPERISPOMENON

print(get_accent_type('ἀγαθοῦ') == PERISPOMENON) # True. NB: get_accent_type returns the accent type of a word as a tuple of the syllable number and accent
print(get_accent_type('ἀγαθοῦ')) # (1, '͂')
print(get_accent_type('ὗσον') == PROPERISPOMENON)

''' formatter module. is it broken???
It gives me this when run on the tokens:
18 characters were changed
\u03c7 (χ) to \u03bd (ν)
\u1f34 (ἴ) to \u0313 (̓)
\u1fde (῞) to \u0020 ( )
\u03bf (ο) to \u03b1 (α)
\u03c2 (ς) to \u03c7 (χ)
\u03c1 (ρ) to \u0301 (́)
\u03bd (ν) to \u0301 (́)
\u03b1 (α) to \u1f34 (ἴ)
\u03b1 (α) to \u1f25 (ἥ)
\u1f25 (ἥ) to \u0314 (̔)
\u1fce (῎) to \u0020 ( )

'''

from cltk.corpus.utils.formatter import cltk_normalize

print(cltk_normalize('\u0386'))



def get_normalized_escape_code(input_str):
    # First, decode the input string's unicode escape sequences
    decoded_str = bytes(input_str, "utf-8").decode("unicode_escape")
    
    # Normalize the decoded string
    normalized_str = cltk_normalize(decoded_str)
    
    # Convert normalized characters back to unicode escape codes
    normalized_escape_codes = ''.join(f"\\u{ord(c):04x}" for c in normalized_str)
    
    return normalized_escape_codes

# Example usage
input_escape_code = "\\u0386" 
normalized_escape_code = get_normalized_escape_code(input_escape_code)
print(f"Original: {input_escape_code}, Normalized Escape Code: {normalized_escape_code}")

input_escape_code2 = "\\u0386" 
normalized_escape_code2 = get_normalized_escape_code(input_escape_code2)
print(f"Original: {input_escape_code2}, Normalized Escape Code: {normalized_escape_code2}")