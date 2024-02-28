import normalize

normalize.normalize_columns('prepare_tokens/tokens/test_norm.txt', 'prepare_tokens/tokens/test_.txt')

TONOS_OXIA_PLUS_DIALYTIKA = {
    '\u03ac': '\u1f71', # ά
    '\u03ad': '\u1f73', # έ
    '\u03ae': '\u1f75', # ή
    '\u03af': '\u1f77', # ί
    '\u03cc': '\u1f79', # ό
    '\u03cd': '\u1f7b', # ύ
    '\u03ce': '\u1f7d', # ώ
    '\u0390': '\u1fd3', # ΐ Greek Small Letter Iota With Dialytika And Oxia; my addition
    '\u03b0': '\u1fe3', # ΰ Greek Small Letter Iota With Dialytika And Oxia; my addition
}

def escape_codes(text):
    return ' '.join(f"\\u{ord(c):04x}" for c in text)

def tonos_oxia_converter(text, reverse=False):
    original_escape_codes = escape_codes(text)
    print(f"Original text: {text}")
    print(f"Original escape codes: {original_escape_codes}")
    for char_tonos, char_oxia in TONOS_OXIA_PLUS_DIALYTIKA.items():
        if not reverse:
            if char_tonos in text:
                print(f"Replacing {char_tonos} with {char_oxia} (\\u{ord(char_tonos):04x} -> \\u{ord(char_oxia):04x})")
            text = text.replace(char_tonos, char_oxia)
        else:
            if char_oxia in text:
                print(f"Replacing {char_oxia} with {char_tonos} (\\u{ord(char_oxia):04x} -> \\u{ord(char_tonos):04x})")
            text = text.replace(char_oxia, char_tonos)
    converted_escape_codes = escape_codes(text)
    print(f"Converted text: {text}")
    print(f"Converted escape codes: {converted_escape_codes}")
    return text

# Directly test the function with a known string
#test_text = "άέήίόύώΐΰ"
#tonos_oxia_converter(test_text)

# Create a test string using the left-hand entries (keys) of the dictionary
test_string = ''.join(TONOS_OXIA_PLUS_DIALYTIKA.keys())

# Optionally, print the test string to verify its contents
print("Test string with tonos characters:", test_string)
print("Escape codes:", ' '.join(f"\\u{ord(c):04x}" for c in test_string))

# Use the tonos_oxia_converter function to convert the test string
converted_string = tonos_oxia_converter(test_string)
print("Converted string with oxia characters:", converted_string)



