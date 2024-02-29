'''
In these patterns, all tonos have been substituted by oxia,
using the following script:

# Define tonos to oxia mappings
tonos_to_oxia_mappings = {
    "\u03ac": "\u1f71",  # ά to ά
    "\u03af": "\u1f77",  # ί to ί
    "\u03cd": "\u1f7b",  # ύ to ύ
}

changes_made = False  # Flag to track if any changes are made

# Iterate through each pattern and substitute tonos characters with oxia
for key, pattern in patterns.items():
    original_pattern = pattern  # Keep the original pattern for comparison
    for tonos, oxia in tonos_to_oxia_mappings.items():
        pattern = pattern.replace(tonos, oxia)
    patterns[key] = pattern
    if pattern != original_pattern:  # Check if the pattern was changed
        changes_made = True
        print(f"Substitution made in pattern '{key}'")
    else:
        print(f"No substitution needed for pattern '{key}'")

# Inform about the overall changes
if changes_made:
    print("One or more substitutions were made.")
else:
    print("No substitutions were made in any patterns.")

# Write the modified patterns to a new file
with open('test_filter2.py', 'w') as file:
    file.write("patterns = {\n")
    for key, pattern in patterns.items():
        file.write(f"    '{key}': r'{pattern}',\n")
    file.write("}\n")

print("Modified patterns have been written to test_filter2.py")

'''

patterns = {
    'diphth_y': r'(α|ε|η|ο)(ὐ|ὔ|υ|ὑ|ύ|ὖ|ῦ|ὕ|ὗ|ὺ|ὒ|ὓ)',
    'diphth_i': r'(α|ε|ο|υ)(ἰ|ί|ι|ῖ|ἴ|ἶ|ἵ|ἱ|ἷ|ὶ|ἲ|ἳ)',
    'adscr_i': r'(α|η|ω|ἀ|ἠ|ὠ|ἁ|ἡ|ὡ|ά|ή|ώ|ὰ|ὴ|ὼ|ᾶ|ῆ|ῶ|ὤ|ὥ|ὢ|ὣ|ἄ|ἅ|ἂ|ἃ|ἤ|ἥ|ἣ|ἢ|ἦ|ἧ|ἆ|ἇ|ὧ|ὦ)(ι)',
    'subscr_i': r'(ᾄ|ᾂ|ᾆ|ᾀ|ᾅ|ᾃ|ᾇ|ᾁ|ᾴ|ᾲ|ᾶ|ᾷ|ᾳ|ᾔ|ᾒ|ᾖ|ᾐ|ᾕ|ᾓ|ᾗ|ᾑ|ῄ|ῂ|ῃ|ᾤ|ᾢ|ᾦ|ᾠ|ᾥ|ᾣ|ᾧ|ᾡ|ῴ|ῲ|ῷ|ῳ|ῇ)',
    'stops': r'[πκτβδγφχθ]',
    'liquids': r'[ρλῥ]',
    'nasals': r'[μν]',
    'double_cons': r'[ζξψ]',
    'sibilants': r'[σς]',
    'vowels': r'[αεηιυωοἀἁἐἑἰἱὀὁἠἡὐὑὠὡάὰέὲήὴόὸίὶὺύώὼἄἅἔἕὄὅὂὃἤἥἴἵὔὕὤὥἂἃἒἓἢἣἲἳὒὓὢὣᾶῆῖῦῶἇἆἦἧἶἷὖὗὦὧϋϊΐῒϋῢΰῗῧ]',
}
