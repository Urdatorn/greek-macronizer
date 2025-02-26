patterns = {
    'diphth_y': r'(α|ε|η|ο)(ὐ|ὔ|υ|ὑ|ύ|ὖ|ῦ|ὕ|ὗ|ὺ|ὒ|ὓ)',
    'diphth_i': r'(α|ε|ο|υ)(ἰ|ί|ι|ῖ|ἴ|ἶ|ἵ|ἱ|ἷ|ὶ|ἲ|ἳ)',
    'adscr_i': r'(α|η|ω|ἀ|ἠ|ὠ|ἁ|ἡ|ὡ|ά|ή|ώ|ὰ|ὴ|ὼ|ᾶ|ῆ|ῶ|ὤ|ὥ|ὢ|ὣ|ἄ|ἅ|ἂ|ἃ|ἤ|ἥ|ἣ|ἢ|ἦ|ἧ|ἆ|ἇ|ὧ|ὦ)(ι)',
    'subscr_i': r'(ᾄ|ᾂ|ᾆ|ᾀ|ᾅ|ᾃ|ᾇ|ᾁ|ᾴ|ᾲ|ᾷ|ᾳ|ᾔ|ᾒ|ᾖ|ᾐ|ᾕ|ᾓ|ᾗ|ᾑ|ῄ|ῂ|ῃ|ᾤ|ᾢ|ᾦ|ᾠ|ᾥ|ᾣ|ᾧ|ᾡ|ῴ|ῲ|ῷ|ῳ|ῇ)',
    'stops': r'[πκτβδγφχθ]',
    'liquids': r'[ρλῥ]',
    'nasals': r'[μν]',
    'double_cons': r'[ζξψ]',
    'sibilants': r'[σς]',
    'vowels': r'[αεηιυωοἀἁἐἑἰἱὀὁἠἡὐὑὠὡάὰέὲήὴόὸίὶὺύώὼἄἅἔἕὄὅὂὃἤἥἴἵὔὕὤὥἂἃἒἓἢἣἲἳὒὓὢὣᾶῆῖῦῶἇἆἦἧἶἷὖὗὦὧϋϊΐῒϋῢΰῗῧ]'
}

text = "άέήίόύώ"
for char in text:
    code_point = ord(char)
    print(f"Character: {char}, Unicode escape sequence: \\u{code_point:04x}")