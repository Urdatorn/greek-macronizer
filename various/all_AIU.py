'''
All 108 different AIY in cltk, including unnecessary
- long iota subscriptum forms
- macronized lower-case forms without other diacritics 
- circumflexes

'''
AIY = set([
    # CAPITALS
    "\u0391",  # Α Greek Capital Letter Alpha
    "\u0399",  # Ι Greek Capital Letter Iota
    "\u03a5",  # Υ Greek Capital Letter Upsilon
    "\u1fbc",  # ᾼ Greek Capital Letter Alpha with Prosgegrammeni

    "\u0386",  # Ά Greek Capital Letter Alpha with Tonos
    "\u038a",  # Ί Greek Capital Letter Iota with Tonos
    "\u038e",  # Ύ Greek Capital Letter Upsilon with Tonos

    "\u1fba",  # Ὰ Greek Capital Letter Alpha with Varia
    "\u1fda",  # Ὶ Greek Capital Letter Iota with Varia
    "\u1fea",  # Ὺ Greek Capital Letter Upsilon with Varia

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

    "\u1fb9",  # Ᾱ Greek Capital Letter Alpha With Macron
    "\u1fd9",  # Ῑ Greek Capital Letter Iota With Macron
    "\u1fe9",  # Ῡ Greek Capital Letter Upsilon With Macron

    "\u1fb8",  # Ᾰ Greek Capital Letter Alpha With Vrachy
    "\u1fd8",  # Ῐ Greek Capital Letter Iota With Vrachy
    "\u1fe8",  # Ῠ Greek Capital Letter Upsilon With Vrachy

    # LOWER-CASE
    "\u03b1",  # α Greek Small Letter Alpha
    "\u03b9",  # ι Greek Small Letter Iota
    "\u03c5",  # υ Greek Small Letter Upsilon
    "\u1fb3",  # ᾳ Greek Small Letter Alpha With Ypogegrammeni

    "\u03ac",  # ά Greek Small Letter Alpha With Tonos
    "\u03af",  # ί Greek Small Letter Iota With Tonos
    "\u03cd",  # ύ Greek Small Letter Upsilon With Tonos
    "\u1fb4",  # ᾴ Greek Small Letter Alpha With Oxia And Ypogegrammeni

    "\u1f70",  # ὰ Greek Small Letter Alpha With Varia
    "\u1f76",  # ὶ Greek Small Letter Iota With Varia
    "\u1f7a",  # ὺ Greek Small Letter Upsilon With Varia
    "\u1fb2",  # ᾲ Greek Small Letter Alpha With Varia And Ypogegrammeni

    "\u1fb6",  # ᾶ Greek Small Letter Alpha With Perispomeni
    "\u1fd6",  # ῖ Greek Small Letter Iota With Perispomeni
    "\u1fe6",  # ῦ Greek Small Letter Upsilon With Perispomeni
    "\u1fb7",  # ᾷ Greek Small Letter Alpha With Perispomeni And Ypogegrammeni

    "\u1f00",  # ἀ Greek Small Letter Alpha With Psili
    "\u1f30",  # ἰ Greek Small Letter Iota With Psili
    "\u1f50",  # ὐ Greek Small Letter Upsilon With Psili
    "\u1f80",  # ᾀ Greek Small Letter Alpha With Psili And Ypogegrammeni

    "\u1f04",  # ἄ Greek Small Letter Alpha With Psili And Oxia
    "\u1f34",  # ἴ Greek Small Letter Iota With Psili And Oxia
    "\u1f54",  # ὔ Greek Small Letter Upsilon With Psili And Oxia
    "\u1f84",  # ᾄ Greek Small Letter Alpha With Psili And Oxia And Ypogegrammeni

    "\u1f02",  # ἂ Greek Small Letter Alpha With Psili And Varia
    "\u1f32",  # ἲ Greek Small Letter Iota With Psili And Varia
    "\u1f52",  # ὒ Greek Small Letter Upsilon With Psili And Varia
    "\u1f82",  # ᾂ Greek Small Letter Alpha With Psili And Varia And Ypogegrammeni

    "\u1f06",  # ἆ Greek Small Letter Alpha With Psili And Perispomeni
    "\u1f36",  # ἶ Greek Small Letter Iota With Psili And Perispomeni
    "\u1f56",  # ὖ Greek Small Letter Upsilon With Psili And Perispomeni
    "\u1f86",  # ᾆ Greek Small Letter Alpha With Psili And Perispomeni And Ypogegrammeni

    "\u1f01",  # ἁ Greek Small Letter Alpha With Dasia
    "\u1f31",  # ἱ Greek Small Letter Iota With Dasia
    "\u1f51",  # ὑ Greek Small Letter Upsilon With Dasia
    "\u1f81",  # ᾁ Greek Small Letter Alpha With Dasia And Ypogegrammeni

    "\u1f05",  # ἅ Greek Small Letter Alpha With Dasia And Oxia
    "\u1f35",  # ἵ Greek Small Letter Iota With Dasia And Oxia
    "\u1f55",  # ὕ Greek Small Letter Upsilon With Dasia And Oxia
    "\u1f85",  # ᾅ Greek Small Letter Alpha With Dasia And Oxia And Ypogegrammeni

    "\u1f03",  # ἃ Greek Small Letter Alpha With Dasia And Varia
    "\u1f33",  # ἳ Greek Small Letter Iota With Dasia And Varia
    "\u1f53",  # ὓ Greek Small Letter Upsilon With Dasia And Varia
    "\u1f83",  # ᾃ Greek Small Letter Alpha With Dasia And Varia And Ypogegrammeni

    "\u1f07",  # ἇ Greek Small Letter Alpha With Dasia And Perispomeni
    "\u1f37",  # ἷ Greek Small Letter Iota With Dasia And Perispomeni
    "\u1f57",  # ὗ Greek Small Letter Upsilon With Dasia And Perispomeni
    "\u1f87",  # ᾇ Greek Small Letter Alpha With Dasia And Perispomeni And Ypogegrammeni

    "\u03ca",  # ϊ Greek Small Letter Iota With Dialytika
    "\u03cb",  # ϋ Greek Small Letter Upsilon With Dialytika

    "\u0390",  # ΐ Greek Small Letter Iota With Dialytika And Tonos
    "\u03b0",  # ΰ Greek Small Letter Upsilon With Dialytika And Tonos

    "\u1fd2",  # ῒ Greek Small Letter Iota With Dialytika And Varia
    "\u1fe2",  # ῢ Greek Small Letter Upsilon With Dialytika And Varia
 
    "\u1fd7",  # ῗ Greek Small Letter Iota With Dialytika And Perispomeni
    "\u1fe7",  # ῧ Greek Small Letter Upsilon With Dialytika And Perispomeni

    "\u1fb1",  # ᾱ Greek Small Letter Alpha With Macron
    "\u1fd1",  # ῑ Greek Small Letter Iota With Macron
    "\u1fe1",  # ῡ Greek Small Letter Upsilon With Macron

    "\u1fb0",  # ᾰ Greek Small Letter Alpha With Vrachy
    "\u1fd0",  # ῐ Greek Small Letter Iota With Vrachy
    "\u1fe0",  # ῠ Greek Small Letter Upsilon With Vrachy
])