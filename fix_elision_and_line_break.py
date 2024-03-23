'''
Fixes elided tokens whose elision signs have become separate tokens, 
as well as words with intra-word line breaks which have been triply tokenized: first part of the word + en dash + last part.

### CONTEXT AND THEORY ###

To understand the way in which the tokens have been extracted and the artifacts created thereby is crucial.
Take as an exampe Soph. Ajax 699f, Νύσια Κνώσι᾽ ὀρχήματ᾽ αὐτοδαῆ ξυνὼν ἰάψῃς:

Νύσια	a-p---na-	Νύσιος
Κνώσι	n-p---na-	Κνώσι
’	n-p---na-	’
ὀρ	n-p---na-	ὀρ
-	u--------	-
χήματ	n-p---na-	χήματ
’	n-p---na-	’
αὐτοδαῆ	a-p---na-	αὐτοδαής
ξυνὼν	v-sppamn-	ξυνὼν
ἰάψῃς	v2sasa---	ἰάπτω

Obviously, words followed by a line with an elision mark, need to be reunited with this mark (Κνώσι, χήματ + ’),
and words encircling a line-break mark need to be joined together (ὀρ + χήματ).

Now, the use of dashes for ellipses could have created confusion, as e.g. Eur. IT 1, 23, "τίκτει — τὸ καλλιστεῖον εἰς ἔμ᾽ ἀναφέρων —"

—	u--------	—
τὸ	l-s---na-	ὁ
καλλιστεῖον	n-s---na-	καλλιστεῖον
εἰς	r--------	εἰς
ἔμ	p-s---ma-	ἔμ
’	p-s---ma-	’
ἀναφέρων	v-sppamn-	ἀναφέρω
—	u--------	—

Luckily, the two usages have (hopefully consistently!) separate unicodes: the line-break is a short en dash, same as in the tag,
while the ellipsis is surrounded by two em dashes. 

WHAT IS ELISION IN GREEK?

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